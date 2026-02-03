from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.database import Base

class Unified(Base):
    __tablename__ = "unified"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String)
    provider_id = Column(Integer, unique=True)
    created_at = Column(DateTime)
    amount = Column(Integer)
    currency = Column(String)
    status = Column(String)