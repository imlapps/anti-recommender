from app.models import User
from app.models.types import NonBlankString, RecordKey


class UserState(User):
    """
    Pydantic model to hold the state of a `User`.

    `anti_recommendations_history` is the history of all anti-recommendations a user has seen.
    """

    anti_recommendations_history: dict[NonBlankString, RecordKey]
