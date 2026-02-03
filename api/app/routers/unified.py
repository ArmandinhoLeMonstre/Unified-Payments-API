from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_fernet, get_redis_client
from app.models.unified_model import Unified
from app.schemas.unified_schema import SyncRequest
import app.services.unified_service as unified_service

router = APIRouter(prefix="/sync")

@router.post("/")
def sync(
    sync_request: SyncRequest, 
    fernet = Depends(get_fernet), 
    db : Session = Depends(get_db), 
    redis_client = Depends(get_redis_client)
):
    return unified_service.unified_service(sync_request, fernet, db, redis_client)
