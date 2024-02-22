from __future__ import annotations

from abc import ABC, abstractmethod


class Record(ABC):
    """An interface for an immutable storage of records."""

    @abstractmethod
    def get_record(self: Record) -> tuple[dict, ...]:
        """Return a record from storage."""
