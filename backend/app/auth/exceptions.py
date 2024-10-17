from abc import ABC, abstractmethod


class AuthInvalidCredentialsException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        pass


class UserException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        pass
