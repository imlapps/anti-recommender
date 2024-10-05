from datetime import UTC, datetime

from app.models import User
from app.models.types import RecordKey


class UserState(User):
    created_at: datetime = datetime.now(UTC)
    anti_recommendations_history: dict[str, RecordKey]
    last_updated: datetime = datetime.now(UTC)
