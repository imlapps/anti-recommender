from abc import ABC, abstractmethod

from app.models import AuthToken


class AuthResponse(ABC):
    """An interface for a response received in an AuthService."""

    @property
    @abstractmethod
    def authentication_token(self) -> AuthToken:
        pass
