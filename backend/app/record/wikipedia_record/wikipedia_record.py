from __future__ import annotations

from app.record.record import Record


class WikipediaRecord(Record):
    """A concerete implementation of Record.

    Obtain a tuple of Wikipedia records and preserve it in storage.
    """

    def __init__(self: WikipediaRecord, records: tuple[dict, ...]) -> None:
        """Initialize WikipediaRecord and preserve records in storage."""
        self.wikipedia_record = records

    def get_record(self: WikipediaRecord, record_key: str) -> tuple[dict, ...] | None:
        """Return a Wikipedia record from storage."""
        if record_key not in self.wikipedia_record[0]:
            return None

        return ({record_key: self.wikipedia_record[0][record_key]},)
