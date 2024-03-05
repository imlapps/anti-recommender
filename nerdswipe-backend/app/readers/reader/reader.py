from collections.abc import Generator
from abc import ABC, abstractmethod

from app.models.record import Record


class Reader(ABC):
    """ An interface to read and parse records from storage."""

    @abstractmethod
    def read(self) -> Generator[Record, None, None]:
        """Read in output data and yield Records."""
