from abc import ABC, abstractmethod

from app.models import Token


class AuthResult(ABC):
    @property
    @abstractmethod
    def succeeded(self) -> bool:
        pass

    @property
    @abstractmethod
    def authentication_token(self) -> Token:
        pass


class UserResult(ABC):
    @property
    @abstractmethod
    def succeeded(self) -> bool:
        pass

    @property
    @abstractmethod
    def user_id(self) -> str:
        pass
