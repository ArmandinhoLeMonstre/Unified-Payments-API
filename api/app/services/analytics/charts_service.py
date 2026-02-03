import app.services.db_services.retrieve_service as retrieve_service
from app.services.redis.redis_class import RedisCache
from app.models.unified_model import Unified
from app.schemas.charts_schema import ChartsResponse
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone
import json

def retrieve_charts_cache(redis):
    charts = redis.get_cache("chart") #Maybe do a .env variable for redis variables, then add to settings

    if charts is None:
        return None

    charts=json.loads(charts)

    response = ChartsResponse(chart=charts)

    return (response)

def set_charts_cache(redis, final):
    chart_json = json.dumps(final)

    try:
        redis.set_cache("chart", chart_json)
    except Exception as e:
        print(f"Redis cache failed in charts: {e}")
        return None

    return(0)

def get_data_for_charts(db, redis_client):
    redis = RedisCache(redis_client)

    cache = retrieve_charts_cache(redis)
    if cache:
        return cache

    filters = []
    
    start = (datetime.now(timezone.utc) - timedelta(days=10)).date()
    end = datetime.now(timezone.utc).date()

    filters.append(func.date(Unified.created_at) <= end)
    filters.append(func.date(Unified.created_at) >= start)

    response = retrieve_service.count_transaction(filters, db)

    res = {day: transactions for day,transactions in response}
    final = {}
    current = start

    while current <= end:
        day_str = current.isoformat()
        final[day_str] = res.get(day_str, 0)
        current += timedelta(days=1)
    
    set_charts_cache(redis, final)

    response = ChartsResponse(chart=final)

    return(response)

def get_data_per_day(providers, db):

    start = (datetime.now(timezone.utc) - timedelta(days=10)).date()
    end = datetime.now(timezone.utc).date()

    filters = []
    filters.append(Unified.provider.in_(providers))
    filters.append(func.date(Unified.created_at) >= start)
    filters.append(Unified.status == "succeeded")
    response = retrieve_service.get_revenue_per_day(filters, db)

    final = {}
    current = start

    while current <= end:
        day_str = current.isoformat()
        final[day_str] = {}
        current += timedelta(days=1)

    for day, amount, currency in response:
        final[day][currency] = amount

    print(response)
    print(final)

    return(final)