from abc import ABC, abstractmethod

from app.auth import AuthResponse, UserResponse
from app.models import AuthToken, Credentials


class AuthService(ABC):
    """An interface to authenticate a User on the NerdSwipe backend."""

    @abstractmethod
    def get_user(self, *, authentication_token: AuthToken) -> UserResponse:
        raise NotImplementedError

    @abstractmethod
    def sign_in(self, *, authentication_credentials: Credentials) -> AuthResponse:
        raise NotImplementedError

    @abstractmethod
    def sign_in_anonymously(self) -> AuthResponse:
        raise NotImplementedError

    @abstractmethod
    def sign_out(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def sign_up(self, *, authentication_credentials: Credentials) -> AuthResponse:
        raise NotImplementedError
