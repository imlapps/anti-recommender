from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from app.record.record.wikipedia_record.wikipedia_record import WikipediaRecord
from app.record.record_reader.wikipedia_record_reader.wikipedia_record_reader import (
    WikipediaRecordReader,
)
from app.record.record_service.record_service import RecordService


@pytest.fixture(scope="module")
def wikipedia_records() -> tuple[dict[str, dict[str, str]]]:
    """Return a tuple containing sample Wikipedia records."""
    return ({
        "test-wikipedia-article-1": {
            "test-info": "test info for test-wikipedia-article-1",
        },
    },)


@pytest.fixture(scope="module")
def wikipedia_record(wikipedia_records: tuple[dict[str, dict[str, str]]]) -> WikipediaRecord:  # noqa: E501
    """Yield a WikipediaRecord object."""
    return WikipediaRecord(wikipedia_records)


@pytest.fixture(scope="module")
def first_wikipedia_record_item(wikipedia_records: tuple[dict[str, dict[str, str]]]) -> tuple[dict[str, dict[str, str]]]:  # noqa: E501
    """Return a tuple containing the first item in wikipedia_records."""
    return ({next(iter(wikipedia_records[0].keys())):
             wikipedia_records[0][next(iter(wikipedia_records[0].keys()))],
             },)


@pytest.fixture(scope="module")
def record_service() -> RecordService:
    """Yield a RecordService object."""
    return RecordService()


@pytest.fixture(scope="module")
def wikipedia_record_reader() -> WikipediaRecordReader:
    """Return a fixture for WikipediaRecordReader."""
    return WikipediaRecordReader()


@pytest.fixture(scope="module")
def wikipedia_output_path() -> Path:
    """Return the Path of the Wikipedia output file."""
    load_dotenv()

    return (
        Path(__file__).parent.parent.parent
        / "data"
        / os.getenv("WIKIPEDIA_OUTPUT_FILE_NAME")
    )
