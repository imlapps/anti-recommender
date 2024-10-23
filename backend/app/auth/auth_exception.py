from abc import ABC, abstractmethod


class AuthException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        pass
