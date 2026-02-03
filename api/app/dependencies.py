from app.core.settings import settings
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from starlette.requests import Request
from cryptography.fernet import Fernet
import redis
import os

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_fernet():
    key = settings.encryption_key
    f = Fernet(key)

    return (f)

def get_redis_client():
    client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True
    )

    return(client)