from abc import ABC, abstractmethod

from app.auth.results import AuthResult, UserResult
from app.models import Credentials, Token


class AuthService(ABC):
    @abstractmethod
    def get_user(self, authentication_token: Token) -> UserResult:
        pass

    @abstractmethod
    def sign_in(self, authentication_credentials: Credentials) -> AuthResult:
        pass

    @abstractmethod
    def sign_out(self) -> AuthResult:
        pass

    @abstractmethod
    def sign_up(self, authentication_credentials: Credentials) -> AuthResult:
        pass
