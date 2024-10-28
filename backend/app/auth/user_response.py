from abc import ABC, abstractmethod

from app.models.types import UserId


class UserResponse(ABC):
    """An interface for a response that contains user information obtained from an AuthService."""

    @property
    @abstractmethod
    def succeeded(self) -> bool:
        """Returns True if user information is present, and False otherwise."""

        raise NotImplementedError

    @property
    @abstractmethod
    def user_id(self) -> UserId | None:
        """The user ID of an authenticated user."""

        raise NotImplementedError
