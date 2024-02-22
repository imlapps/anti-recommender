from __future__ import annotations

from abc import ABC, abstractmethod


class Record(ABC):
    """An interface for an immutable storage of records."""

    @abstractmethod
    def __init__(self: Record, records: tuple[dict, ...]) -> None:
        """Initialize Record and obtain records to preserve in storage."""

    @abstractmethod
    def get_record(self: Record, record_key: str | None) -> tuple[dict, ...] | None:
        """Return a record from storage."""

    @abstractmethod
    def get_first_record(self: Record) -> tuple[dict, ...] | None:
        """Return the first record from storage."""
