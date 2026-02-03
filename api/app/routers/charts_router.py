from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import app.services.analytics.charts_service as charts_service
from app.dependencies import get_db, get_redis_client
from app.schemas.charts_schema import ChartsResponse
from typing import List

router = APIRouter(prefix="/charts")

@router.get("/")
def get_charts_data(db : Session = Depends(get_db), redis_client = Depends(get_redis_client)):
    response = charts_service.get_data_for_charts(db, redis_client)
    return (response)

@router.get("/revenues")
def get_chars_revenue_per_day_and_currency(providers: List[str] = Query(default=[]), db : Session = Depends(get_db)):
    response = charts_service.get_data_per_day(providers, db)
    return (response)