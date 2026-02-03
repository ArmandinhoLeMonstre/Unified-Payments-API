from app.dependencies import get_fernet
from app.models.provider_model import ProviderCredential
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy import select

def store_key(provider, key, db):
    if isinstance(key, bytes):
        key = key.decode("utf-8")

    provider_credential = ProviderCredential(provider=provider, api_key=key)

    try:
        db.add(provider_credential)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Database error, couldn't update provider {provider}"
        )

    return(0)

def retrieve_key(provider, db):
    final_key = None
    stmt = select(ProviderCredential.api_key).where(ProviderCredential.provider == provider)
    key = db.execute(stmt).mappings().first()

    if key:
        final_key = key.api_key

    return(final_key)