from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.database import Base

class ProviderState(Base):
    __tablename__ = "providers_state"

    id = Column(Integer, primary_key=True)
    provider = Column(String, unique=True)
    active = Column(Boolean)
    last_synced_at = Column(DateTime, nullable=True)

class ProviderCredential(Base):
    __tablename__ = "providers_credentials"

    id = Column(Integer, primary_key=True)
    provider = Column(String, unique=True)
    api_key = Column(String)