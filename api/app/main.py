from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.settings import settings
from app.core.security import try_encryption_key
from app.routers.unified import router as unified_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.charts_router import router as charts_router
from app.routers.settings_router import router as settings_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.init import init_db, init_providers_default_data
from contextlib import asynccontextmanager
import redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    try_encryption_key()
    init_db()
    init_providers_default_data()

    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8081",
    "http://localhost:5173",
    "http://192.168.69.240:8081",
    "http://192.168.69.240:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(unified_router)
app.include_router(dashboard_router)
app.include_router(charts_router)
app.include_router(settings_router)