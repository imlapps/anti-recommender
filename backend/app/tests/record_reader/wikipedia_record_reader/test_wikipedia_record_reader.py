import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from app.record_reader.wikipedia_record_reader.wikipedia_record_reader import (
    WikipediaRecordReader,
)

load_dotenv()

WIKIPEDIA_OUTPUT_PATH = (
    Path(__file__).parent.parent.parent.parent
    / "data"
    / os.getenv("WIKIPEDIA_OUTPUT_FILE_NAME")
)


@pytest.fixture()
def wikipedia_record_reader() -> WikipediaRecordReader:
    """Return a fixture for WikipediaRecordReader."""
    return WikipediaRecordReader()


@pytest.mark.parametrize(
    ("test_file_path", "expected_output"), [
        (WIKIPEDIA_OUTPUT_PATH, tuple), (Path("test_path"), int)],
)
def test_load_json_data(wikipedia_record_reader: WikipediaRecordReader, test_file_path: Path, expected_output: type) -> None:  # noqa: E501
    """Test that WikipediaRecord.load_json_data() returns the expected output type."""
    assert type(wikipedia_record_reader.load_json_data(  # noqa: S101
        test_file_path)) == expected_output
