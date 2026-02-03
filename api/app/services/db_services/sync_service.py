from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.unified_model import Unified
from app.models.provider_model import ProviderState
from datetime import datetime, timezone

def create_data(data, db: Session):
    data = list(data)
    for d in data:
        try:
            db.add(d)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=500, 
                detail="Database error while adding in create_data"
            )

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="Database error during creating data"
        )

    return (len(data))

def sync_state_update(provider_name, db: Session):

    stmt = select(ProviderState).where(ProviderState.provider == provider_name)
    synced_object = db.scalars(stmt).first()

    last_synced_at = datetime.now(timezone.utc)

    synced_object.last_synced_at = last_synced_at

    try:
        db.add(synced_object)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="Database error while adding in sync_state"
        )

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="Database error while commiting in sync_state"
        )
    return (0)

def check_last_synced_at(provider, db : Session):
    last_synced_at = None

    stmt = select(ProviderState).where(ProviderState.provider == provider)
    synced_object = db.execute(stmt).scalar_one_or_none()

    if (synced_object.last_synced_at):
        last_synced_at = synced_object.last_synced_at
    print(f" last_sync {last_synced_at}")
    return (last_synced_at)

def set_provider_active(provider, db):

    stmt = select(ProviderState).where(ProviderState.provider == provider)
    synced_object = db.execute(stmt).scalar_one_or_none()

    synced_object.active = True

    try:
        db.add(synced_object)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="Database error while updating provider active status"
        )

    return(0)

def check_provider_state(provider, db):
    stmt = select(ProviderState.active).where(ProviderState.provider == provider)
    provider_state = db.execute(stmt).scalar_one_or_none()

    return(provider_state)