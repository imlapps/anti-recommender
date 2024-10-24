from abc import ABC, abstractmethod

from app.models.types import NonBlankString


class AuthException(ABC, BaseException):
    """An interface for an exception encountered in an AuthService."""

    @property
    @abstractmethod
    def message(self) -> NonBlankString:
        pass
