
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from app.models.record import Record
from app.readers.reader.wikipedia_reader.wikipedia_reader import WikipediaReader


@pytest.fixture()
def wikipedia_output_path() -> Path:
    """Return the Path of the Wikipedia output file."""
    load_dotenv()

    return Path(__file__).parent.parent.parent.parent / "data" / os.getenv("WIKIPEDIA_OUTPUT_FILE_NAME")


@pytest.fixture()
def wikipedia_reader(wikipedia_output_path: Path) -> WikipediaReader:
    """Yield a WikipediaReader object."""

    return WikipediaReader(file_path=wikipedia_output_path)


def test_read(wikipedia_reader: WikipediaReader) -> None:
    """Test that WikipediaReader.read() yields the expected output type."""

    assert isinstance(next(wikipedia_reader.read(), None), Record)
