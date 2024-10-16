from abc import ABC, abstractmethod


class AuthInvalidCredentialsException(BaseException, ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        pass


class UserException(BaseException, ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        pass
