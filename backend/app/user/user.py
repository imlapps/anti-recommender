from abc import ABC, abstractmethod
from collections.abc import Iterable

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from app.user import UserService
from app.models.types import NonBlankString, RecordKey
from dataclasses import dataclass


@dataclass
class User:
    """
    Pydantic model that contains information of a User.

    `id` is the UUID of the User.
    """

    id: Annotated[UUID, Field(..., alias="user_id")]
    _service: UserService

    @property
    def last_seen_record_key(self) -> RecordKey:
        return self._service.get_user_last_seen_anti_recommendation(self.id)

    def register_user(self) -> None:
        pass

    def update_anti_recommendations_history(
        self, anti_recommendation_key: RecordKey
    ) -> None:
        self._service.update_user_anti_recommendations_history(
            user_id=self.id, anti_recommendation_key=anti_recommendation_key
        )

    def delete_user(self) -> None:
        self._service.delete_user(user_id=self.id)

    def anti_recommendations_history(self) -> tuple[RecordKey, ...]:
        return self._service.get_user_anti_recommendations_history(self.id)
