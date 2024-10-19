from abc import ABC, abstractmethod


class DatabaseException(ABC, BaseException):
    @property
    @abstractmethod
    def message(self) -> str:
        pass
