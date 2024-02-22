from __future__ import annotations

from app.record.record.record import Record


class WikipediaRecord(Record):
    """A concerete implementation of Record.

    Obtain a tuple of Wikipedia records and preserve it in storage.
    """

    def __init__(self: WikipediaRecord, records: tuple[dict, ...]) -> None:
        """Initialize WikipediaRecord and preserve records in storage."""
        self.wikipedia_record = records

    def get_record(self: WikipediaRecord, record_key: str | None) -> tuple[dict, ...] | None:  # noqa: E501
        """Return a Wikipedia record from storage."""
        if record_key not in self.wikipedia_record[0]:
            return None

        return ({record_key: self.wikipedia_record[0][record_key]},)

    def get_first_record(self: WikipediaRecord) -> tuple[dict, ...] | None:
        """Return the first Wikipedia record from storage."""
        if self.wikipedia_record:
            return ({next(iter(self.wikipedia_record[0].keys())): self.wikipedia_record[0][next(iter(self.wikipedia_record[0].keys()))]},)  # noqa: E501

        return None
