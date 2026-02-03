from datetime import datetime, timedelta, timezone
from app.models.unified_model import Unified
from sqlalchemy import func

def datetime_from_hours_ago(hours_ago):
    today = datetime.now()
    yesterday = today - timedelta(hours=hours_ago)
    return (yesterday)

def add_timelapse_filter(days_start, days_end):
    filters = []

    if days_start:
        start = (datetime.now(timezone.utc) - timedelta(days=days_start)).date()
        filters.append(func.date(Unified.created_at) >= start)

    if days_end:
        end = (datetime.now(timezone.utc) - timedelta(days=days_end)).date()
    else:
        end = datetime.now(timezone.utc).date()

    filters.append(func.date(Unified.created_at) <= end)

    return (filters)