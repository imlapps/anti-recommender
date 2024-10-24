from abc import ABC, abstractmethod
from app.models.types import NonBlankString


class AuthException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> NonBlankString:
        pass
