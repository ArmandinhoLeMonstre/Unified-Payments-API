from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.security import encryption_service, credentials_service
from app.schemas.settings_schema import ApiKeyRequest, ProviderStatusRequest
from app.services.db_services import keys_storage_service, sync_service
from app.dependencies import get_fernet, get_db

router = APIRouter(prefix="/settings")

PROVIDER_REGISTRY = {
    "stripe": credentials_service.stripe_credentials_test,
    "mollie": credentials_service.mollie_credentials_test
}

@router.post("/key/add")
def add_key(request: ApiKeyRequest, fernet = Depends(get_fernet), db : Session = Depends(get_db)):
    provider_credentials_test = PROVIDER_REGISTRY.get(request.provider)
    provider_credentials_test(request.api_key)

    token = encryption_service.encrypt_data(request.api_key, fernet)
    keys_storage_service.store_key(request.provider, token, db)
    sync_service.set_provider_active(request.provider, db)
    # make a return msg
    return(0)

@router.post("/provider/status")
def get_provider_status(request: ProviderStatusRequest, db : Session = Depends(get_db)):
    response = sync_service.check_provider_state(request.provider, db)
    return(response)