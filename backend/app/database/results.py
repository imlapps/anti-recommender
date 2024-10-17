from abc import ABC, abstractmethod


class CommandResult(ABC):
    @property
    @abstractmethod
    def succeeded(self) -> bool:
        pass


class QueryResult(ABC):
    @property
    @abstractmethod
    def succeeded(self) -> bool:
        pass

    @property
    @abstractmethod
    def data(self) -> tuple:
        pass
