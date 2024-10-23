from abc import ABC, abstractmethod

from app.auth import AuthResponse
from app.models import AuthToken, Credentials


class AuthService(ABC):
    @abstractmethod
    def get_user(self, authentication_token: AuthToken) -> AuthResponse:
        pass

    @abstractmethod
    def sign_in(self, authentication_credentials: Credentials) -> AuthResponse:
        pass

    @abstractmethod
    def sign_in_anonymously(self) -> AuthResponse:
        pass

    @abstractmethod
    def sign_out(self) -> AuthResponse:
        pass

    @abstractmethod
    def sign_up(self, authentication_credentials: Credentials) -> AuthResponse:
        pass
