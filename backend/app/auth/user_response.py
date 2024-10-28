from abc import ABC, abstractmethod

from app.models.types import UserId


class UserResponse(ABC):
    """An interface for a response that contains User information."""

    @property
    @abstractmethod
    def user_id(self) -> UserId | None:
        """The user ID of an authenticated user."""

        raise NotImplementedError
