from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.models.types import RecordKey
from app.user import UserService


@dataclass(frozen=True)
class User:
    """
    Pydantic model that contains information of a User.

    `id` is the UUID of the User.
    `_service` manages the state of the User.
    """

    id: Annotated[UUID, Field(..., alias="user_id")]
    _service: UserService

    @property
    def anti_recommendations_history(self) -> tuple[RecordKey, ...]:
        """The anti-recommendations history of a `User`."""

        return self._service.get_user_anti_recommendations_history(self.id)

    @property
    def last_seen_anti_recommendation_key(self) -> RecordKey:
        """The last anti-recommendation that was seen by a `User`."""

        return self._service.get_user_last_seen_anti_recommendation(self.id)

    def add_anti_recommendation_to_history(
        self, anti_recommendation_key: RecordKey
    ) -> None:
        """Add `anti_recommendation_key` to a `User` history."""

        self._service.add_to_user_anti_recommendations_history(
            user_id=self.id, anti_recommendation_key=anti_recommendation_key
        )

    def remove_anti_recommendations_slice_from_history(
        self, *, start_index: int, end_index: int | None = None
    ) -> None:
        """Remove a slice of anti-recommendations from a `User` history."""

        self._service.remove_slice_from_user_anti_recommendations_history(
            user_id=self.id, start_index=start_index
        )
