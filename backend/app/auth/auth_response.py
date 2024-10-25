from abc import ABC, abstractmethod

from app.models import AuthToken
from app.models.types import UserId


class AuthResponse(ABC):
    """An interface for a response received in an AuthService."""

    @property
    @abstractmethod
    def user_id(self) -> UserId:
        """The user ID of the authenticated user."""
        raise NotImplementedError

    @property
    @abstractmethod
    def authentication_token(self) -> AuthToken:
        """A new AuthToken containing parameters from an authenticated user."""
        raise NotImplementedError
