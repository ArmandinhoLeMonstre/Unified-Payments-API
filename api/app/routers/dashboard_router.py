from fastapi import APIRouter, Depends, Query
from typing import List, Annotated
import app.services.dashboard_service as dashboard_service
import app.services.analytics.revenue_service as revenue_service
import app.services.analytics.transactions_service as transactions_service
import app.services.analytics.charts_service as charts_service
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_redis_client
from app.schemas.dashboard_schema import (
    OverviewRequest,
    OverviewResponse,
    RevenueByCurrency,
    RevenueRequest,
    RevenueByCurrencyResponse,
    TransactionsRequest,
    TransactionsResponse,
    TableRequest,
    TableResponse
)

router = APIRouter(prefix="/dashboard")

@router.get("/payments", response_model=List[TableResponse])
def retrieve_payments(request: Annotated[TableRequest, Query()], db : Session = Depends(get_db)):
    response = dashboard_service.get_payments(request, db)
    return (response)

@router.get("/last_synced")
def last_synced(db : Session = Depends(get_db)):
    last_synced = dashboard_service.retrieve_last_synced_at(db)
    return (last_synced)

@router.post("/overview", response_model=OverviewResponse)
def get_over(request: OverviewRequest, db : Session = Depends(get_db), redis_client = Depends(get_redis_client)):
    response = dashboard_service.over_service(request, db, redis_client)
    return (response)

@router.post("/revenue/bycurrency", response_model=List[RevenueByCurrencyResponse])
def get_revenue_by_currency(request: RevenueRequest, db : Session = Depends(get_db)):
    response = revenue_service.revenue_by_currency(request, db)
    return (response)

@router.post("/transactions") # Faire un post pour la periode, ex 24 dernieres heures
def get_transactions(request: TransactionsRequest, db : Session = Depends(get_db)):
    response = transactions_service.transactions_service(request, db)
    return (response)