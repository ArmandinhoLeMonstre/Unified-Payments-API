from sqlalchemy.orm import Session
from datetime import datetime
import redis
import json
import app.services.db_services.retrieve_service as retrieve_service
import app.services.db_services.sync_service as sync_service
import app.services.date_service as date_service
import app.services.analytics.revenue_service as revenue_service
from app.services.redis.redis_class import RedisCache
from app.models.unified_model import Unified
from app.schemas.dashboard_schema import (
    OverviewResponse
)

def retrieve_last_synced_at(db : Session):
    data = sync_service.check_last_synced_at("stripe", db)

    return (data)

def get_payments(request, db):
    filters = []

    if request.start or request.end:
        filters = date_service.add_timelapse_filter(request.start, request.end)

    data = retrieve_service.retrieve_for_tab(filters, request.limit, request.offset, db)

    return(data)

def retrieve_overview_cache(redis):

    try:
        revenues = redis.get_cache("revenues")
        transactions = redis.get_cache("transactions")
        last_sync = redis.get_cache("last_sync")
    except Exception as e:
        print(f"Redis cache failed in overview : {e}")
        return None

    if revenues is None or transactions is None or last_sync is None:
        return None

    print("cache overview")

    response = OverviewResponse(
        revenues=json.loads(revenues),
        transactions=int(transactions),
        last_sync=datetime.fromisoformat(last_sync)
    )

    return (response)

def set_overview_cache(redis, revenues, transactions, last_sync):
    revenues_json = json.dumps(revenues)
    value = last_sync.isoformat()

    redis.set_cache("revenues", revenues_json)
    redis.set_cache("transactions", transactions)
    redis.set_cache("last_sync", value)

    return(0)

def over_service(request, db : Session, redis_client):

    redis = RedisCache(redis_client)

    cache = retrieve_overview_cache(redis)
    if cache:
        return(cache)

    filters = []
    #filters = add_filters(start_date, "succeeded", request) # dynamic via request, so we can retrieve pending, failed etc...
    filters.append(Unified.status == "succeeded")
    net_revenue = retrieve_service.sum_amount_by_currency(filters, db)
    print(net_revenue)
    res = {currency: revenue for currency, revenue in net_revenue}
    revenues = net_revenue

    transactions = 0
    filters = []
    filters.append(Unified.status == "succeeded")

    total_transactions = retrieve_service.count_statuses(filters, db)
    amount = 0
    res_trans = {}
    res_trans = {status: count for status, count in total_transactions} # Ici on recoit que une data, refractor
    if res_trans:
        amount = res_trans["succeeded"]

    last_sync = sync_service.check_last_synced_at("stripe", db)

    if last_sync:
        set_overview_cache(redis, res, amount, last_sync)

    response = OverviewResponse(revenues=res, transactions=amount, last_sync=last_sync)

    return (response)