from abc import ABC, abstractmethod


class UserServiceException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        pass
