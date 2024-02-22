from pathlib import Path

from app.record.record_reader.wikipedia_record_reader.wikipedia_record_reader import (
    WikipediaRecordReader,
)


def test_load_json_data(wikipedia_record_reader: WikipediaRecordReader, wikipedia_output_path: Path) -> None:  # noqa: E501
    """Test that WikipediaRecord.load_json_data() returns the expected output type."""
    assert isinstance(type(wikipedia_record_reader.load_json_data(  # noqa: S101
        wikipedia_output_path)[0]), dict)
