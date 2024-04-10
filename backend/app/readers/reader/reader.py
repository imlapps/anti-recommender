from abc import ABC, abstractmethod
from collections.abc import Iterator

from app.models.record import Record


class Reader(ABC):
    """An interface to read and parse Records from storage."""

    @abstractmethod
    def read(self) -> Iterator[Record, None, None]:
        """Read in output data and yield Records."""
