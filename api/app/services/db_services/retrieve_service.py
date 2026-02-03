from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.unified_model import Unified
from app.models.provider_model import ProviderState
from datetime import datetime, timezone

def querry_filters(start_date, request):
    filters = []

    if start_date:
        filters.append(Unified.created_at > start_date)
    
    if request.status:
        filters.append(Unified.status == request.status)
    
    if request.currency:
        filters.append(Unified.currency == request.currency)

    return (filters)

def querry_builder(start_date, request, db : Session):
    filters = querry_filters(start_date, request)
    
    stmt = select(Unified).where(*filters)
    return (stmt)

def retrieve_for_tab(filters, limit, offset, db : Session):
    stmt = (
        select(
            Unified.provider,
            Unified.provider_id,
            Unified.created_at,
            Unified.amount,
            Unified.currency,
            Unified.status
        )
        .where(*filters)
        .order_by(Unified.created_at.desc()).limit(limit).offset(offset)
    )

    rows = db.execute(stmt).mappings().all()

    return (rows)

def sum_amount_by_currency(filters, db : Session):
    stmt = (
        select(Unified.currency, func.sum(Unified.amount).label("total"))
        .where(*filters)
        .group_by(Unified.currency)
        )
    data = db.execute(stmt).all()

    return (data)

def count_statuses(filters, db : Session):
    stmt = (
        select(Unified.status, func.count(Unified.status))
        .where(*filters)
        .group_by(Unified.status)
    )
    data = db.execute(stmt).all()

    return(data)

def count_transaction(filters, db : Session):
    stmt = (
        select(func.date(Unified.created_at), func.count(Unified.id))
        .where(*filters)
        .group_by(func.date(Unified.created_at))
    )
    data = db.execute(stmt).all()

    return(data)

def get_revenue_per_day(filters, db : Session):
    stmt = (
        select(func.date(Unified.created_at), func.sum(Unified.amount), Unified.currency)
        .where(*filters)
        .group_by(func.date(Unified.created_at), Unified.currency)
    )
    data = db.execute(stmt).all()
    return (data)