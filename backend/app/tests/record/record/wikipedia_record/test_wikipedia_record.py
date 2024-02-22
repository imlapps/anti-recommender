from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.record.record.wikipedia_record.wikipedia_record import WikipediaRecord


def test_get_wikipedia_record(wikipedia_record: WikipediaRecord, first_wikipedia_record_item: tuple[dict[str, dict[str, str]]]) -> None:  # noqa: E501
    """Test that WikipediaRecord stores and returns a record from storage."""
    assert wikipedia_record.get_record(                             # noqa: S101
        "test-wikipedia-article-1") == first_wikipedia_record_item


def test_get_wikipedia_record_returns_none(wikipedia_record: WikipediaRecord) -> None:
    """Test that WikipediaRecord returns None when a record does not exist."""
    assert wikipedia_record.get_record("random-wikipedia-article") is None  # noqa: S101


def test_get_first_wikipedia_record(wikipedia_record: WikipediaRecord, first_wikipedia_record_item: tuple[dict[str, dict[str, str]]]) -> None:  # noqa: E501
    """Test that WikipediaRecord returns the first item from storage."""
    assert wikipedia_record.get_first_record() == first_wikipedia_record_item  # noqa: S101
