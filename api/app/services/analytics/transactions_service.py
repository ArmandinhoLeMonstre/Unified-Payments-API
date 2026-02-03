from sqlalchemy.orm import Session
import app.services.db_services.retrieve_service as retrieve_service
import app.services.date_service as date_service
from app.models.unified_model import Unified
from app.schemas.dashboard_schema import (
    TransactionsRequest,
    TransactionsResponse
)

def transactions_service(request, db : Session):
    start_date = date_service.datetime_from_hours_ago(request.hours)

    final = {}

    for provider in request.providers:
        filters = [] 
        filters.append(Unified.provider == provider)
        filters.append(Unified.created_at > start_date)
        filters.append(Unified.status.in_(request.statuses))
        statuses_count = retrieve_service.count_statuses(filters, db)
        res = {status: count for status, count in statuses_count}
        final[provider] = res



    response = TransactionsResponse(transactions=final)
    
    return (response)