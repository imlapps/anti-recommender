from __future__ import annotations

from typing import TYPE_CHECKING

from app.record.record_reader.wikipedia_record_reader.wikipedia_record_reader import (
    WikipediaRecordReader,
)

if TYPE_CHECKING:
    from pytest_mock import MockFixture

    from app.record.record_service.record_service import RecordService


def test_wikipedia_load_data(mocker: MockFixture, record_service: RecordService, wikipedia_records: tuple[dict[str, dict[str, str]]]) -> None:  # noqa: E501
    """Test that RecordService loads Wikipedia data and sets the current title."""
    mocker.patch.object(WikipediaRecordReader, "load_json_data",
                        return_value=wikipedia_records)
    record_service.load_data()

    assert record_service.current_title == "test-wikipedia-article-1"  # noqa: S101


def test_get_record(mocker: MockFixture, record_service: RecordService, wikipedia_records: tuple[dict[str, dict[str, str]]], first_wikipedia_record_item: tuple[dict[str, dict[str, str]]]) -> None:  # noqa: E501
    """Test that RecordService returns the correct record for a given title."""
    mocker.patch.object(WikipediaRecordReader, "load_json_data",
                        return_value=wikipedia_records)
    record_service.load_data()

    assert record_service.get_record(  # noqa: S101
        "test-wikipedia-article-1") == first_wikipedia_record_item


def test_current_title(record_service: RecordService) -> None:
    """Test that RecordService correctly sets the value of current_title."""
    sample_title = "current-title"

    record_service.current_title = sample_title

    assert record_service.current_title == sample_title  # noqa: S101


def test_pop_from_empty_stack(record_service: RecordService) -> None:
    """Test that pop_title_from_stack() returns None when the stack is empty."""
    assert record_service.pop_title_from_stack() is None  # noqa: S101


def test_push_to_stack(record_service: RecordService) -> None:
    """Test that the title popped from the stack matches the last item pushed it."""
    record_service.push_title_to_stack(title="test-wikipedia")
    record_service.push_title_to_stack(title="test-wikipedia-1")

    assert record_service.pop_title_from_stack() == "test-wikipedia-1"  # noqa: S101
