from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from app.record.record.wikipedia_record.wikipedia_record import WikipediaRecord
from app.record.record_reader.wikipedia_record_reader.wikipedia_record_reader import (
    WikipediaRecordReader,
)
from dotenv import load_dotenv

if TYPE_CHECKING:
    from app.record.record.record import Record
    from app.record.record_reader.record_reader import RecordReader


class RecordService:
    """A service that holds and manages the state of Record objects."""

    def __init__(self: RecordService) -> None:
        """Initialize RecordService and its variables."""
        self.__current_title: str | None = ""
        self.__stack: list = []
        self.__record: Record | None = None

    def load_data(self: RecordService) -> None:
        """Load the record and set the current_title to the first record item."""
        load_dotenv()

        output_path: Path
        record_reader: RecordReader | None = None

        if os.getenv("RECORD_TYPE") == "Wikipedia":
            output_path = (
                Path(__file__).parent.parent
                / "data"
                / os.getenv("WIKIPEDIA_OUTPUT_FILE_NAME")
            )

            record_reader = WikipediaRecordReader()
            self.__record = WikipediaRecord(
                record_reader.load_json_data(output_path))

            first_record = self.__record.get_first_record()
            if first_record:
                self.__current_title = next(
                    iter(first_record[0].keys()))

    @property
    def current_title(self: RecordService) -> str | None:
        """Get the title of the current record."""
        return self.__current_title

    @current_title.setter
    def current_title(self: RecordService, title: str = "") -> None:
        """Set the title of the current record."""
        self.__current_title = title

    def get_record(self: RecordService, title: str = "") -> tuple[dict, ...] | None:
        """Return the record of the current title."""
        if self.__record:
            if title:
                return self.__record.get_record(title)
            return self.__record.get_record(self.__current_title)
        return None

    def push_title_to_stack(self: RecordService, title: str = "") -> None:
        """Add a title to the stack."""
        self.__stack.append(title)

    def pop_title_from_stack(self: RecordService) -> str | None:
        """Remove a title from the stack."""
        if self.__stack:
            return self.__stack.pop()

        return None
