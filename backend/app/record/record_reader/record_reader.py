from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class RecordReader(ABC):
    """An interface to read and parse records from storage."""

    @abstractmethod
    def load_json_data(
        self: RecordReader,
        file_path: Path,
    ) -> tuple[dict, ...]:
        """Load and return records from a JSON file."""
