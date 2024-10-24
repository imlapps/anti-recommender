from abc import ABC, abstractmethod

from app.models import AuthToken


class AuthResponse(ABC):
    @property
    @abstractmethod
    def authentication_token(self) -> AuthToken:
        pass
