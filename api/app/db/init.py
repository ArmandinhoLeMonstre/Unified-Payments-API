from app.db.database import Base, engine, SessionLocal
from sqlalchemy import select
from app.models.provider_model import ProviderState
from sqlalchemy.exc import IntegrityError

def init_db():
    Base.metadata.create_all(bind=engine)
    return(0)

def add_provider(provider_name, db):
    stmt = select(ProviderState).where(ProviderState.provider == provider_name)

    data = db.execute(stmt).mappings().all()
    if not data:
        provider = ProviderState(provider=provider_name, active=False, last_synced_at=None)
        try:
            db.add(provider)
        except IntegrityError as e:
            db.rollback()

    return(0)

def init_providers_default_data():
    db = SessionLocal()

    add_provider("mollie", db)
    add_provider("stripe", db)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()

    return(0)
