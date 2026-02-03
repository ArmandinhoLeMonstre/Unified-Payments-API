from app.models.unified_model import Unified
from app.models.provider_model import ProviderState
from app.services.providers.mollie_class import MollieProvider
from app.services.providers.stripe_class import StripeProvider
import app.services.db_services.sync_service as sync_service
import app.services.db_services.keys_storage_service as keys_storage_service
import app.services.security.encryption_service as encryption_service
from app.services.redis.redis_class import RedisCache
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

PROVIDER_REGISTRY = {
    "stripe": StripeProvider,
    "mollie": MollieProvider
}

def convert_to_unified(data, provider_name):
    unified_tab = []

    for d in data:
        Payment = Unified(
            provider=provider_name,
            provider_id=d.get("id"),
            created_at=d.get("date"),
            amount=d.get("amount"),
            currency=d.get("currency"),
            status=d.get("status"))
        
        unified_tab.append(Payment)
    
    return unified_tab

def instantiate_provider_class(provider, last_synced_at, api_key):
    provider_class = PROVIDER_REGISTRY.get(provider)

    if provider_class is None:
        return None

    instance = provider_class(api_key, last_synced_at)

    return (instance)

def handle_providers(provider, last_synced_at, api_key, db):
    instance = instantiate_provider_class(provider, last_synced_at, api_key)

    if not instance:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "class error",
                "code": 403,
            }
        )

    raw = instance.list_payments()
    unified = convert_to_unified(raw, provider)

    return(unified)

def is_provider_active(providers, db):
    for provider in providers:
        provider_state = sync_service.check_provider_state(provider, db)
        if provider_state is False:
            raise HTTPException(
                status_code=409,
                detail=f"{provider} is not active, activate this provider in the settings"
            )

    return(0)

def get_api_key(provider, fernet, db):
    api_key_raw = keys_storage_service.retrieve_key(provider, db)

    if api_key_raw is None:
        raise HTTPException(
            status_code=500,
            detail=f"{provider} is not active, activate this provider in the settings"
        )

    api_key_decrypted = encryption_service.decrypt_data(api_key_raw, fernet)

    return(api_key_decrypted)

def get_last_sync(provider, db):
    last_synced_at = sync_service.check_last_synced_at(provider, db)

    if last_synced_at is None:
        return None

    cooldown = timedelta(minutes=5)
    now = datetime.now()
    diff = now - last_synced_at

    if (diff < cooldown):
        remaining = cooldown - diff
        seconds = int(remaining.total_seconds())
    
        raise HTTPException(
            status_code=429,
            detail=f"you can sync {provider} again in {seconds}"
        )

    return(last_synced_at)

def unified_service(request, fernet, db: Session, redis_client):

    is_provider_active(request.providers, db)

    all_payments = []

    for provider in request.providers:
        last_synced_at = get_last_sync(provider, db)
        api_key = get_api_key(provider, fernet, db)
        unified = handle_providers(provider, last_synced_at, api_key, db)
        all_payments += unified

    print(len(all_payments))
    creations_informations = sync_service.create_data(all_payments, db)

    for provider in request.providers:
        sync_service.sync_state_update(provider, db)

    redis = RedisCache(redis_client)
    redis.clear_all_keys()

    return creations_informations
