from datetime import datetime, timezone
from app.models import User
from backend.app.models.types.record_key import RecordKey
from pydantic import Field


class UserState(User):
    created_at: datetime = datetime.now(timezone.utc)
    anti_recommendations_history: dict[str, RecordKey]
    last_updated: datetime = datetime.now(timezone.utc)
