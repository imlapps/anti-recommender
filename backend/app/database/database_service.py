from abc import ABC, abstractmethod

from app.database.results import CommandResult, QueryResult
from app.models import TableQuery


class DatabaseService(ABC):
    @abstractmethod
    def command(self, table_query: TableQuery) -> CommandResult:
        pass

    @abstractmethod
    def query(self, table_query: TableQuery) -> QueryResult:
        pass
