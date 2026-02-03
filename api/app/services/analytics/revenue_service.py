from sqlalchemy.orm import Session
import app.services.date_service as date_service
import app.services.db_services.retrieve_service as retrieve_service
from app.models.unified_model import Unified
from app.schemas.dashboard_schema import (
    RevenueByCurrencyResponse
)

def add_filters(start_date, status, request):
    filters = []

    if start_date:
        filters.append(Unified.created_at > start_date)
    
    if status:
        filters.append(Unified.status == status)
    
    if hasattr(request, "providers") and request.providers:
        filters.append(Unified.provider.in_(request.providers))
    
    return (filters)

def revenue_by_currency(request, db : Session):
    start_date = date_service.datetime_from_hours_ago(request.hours)

    filters = add_filters(start_date, "succeeded", request) # dynamic via request, so we can retrieve pending, failed etc...
    net_revenue = retrieve_service.sum_amount_by_currency(filters, db)

    tab = []
    res = {currency: revenue for currency, revenue in net_revenue}
    for currency in request.currencies:
        revenue = res.get(currency, None)

        if revenue is not None:
            response = RevenueByCurrencyResponse(currency=currency, revenue=revenue)
            tab.append(response)

    return (tab)
