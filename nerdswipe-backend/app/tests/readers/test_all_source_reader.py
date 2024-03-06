import pytest

from app.models.record.record import Record
from app.readers.all_source_reader import AllSourceReader


@pytest.fixture()
def all_source_reader() -> AllSourceReader:
    """Yield an AllSourceReader object."""
    return AllSourceReader()


def test_read(all_source_reader: AllSourceReader) -> None:
    """Test that AllSourceReader.read() yields the expected output type."""
    assert isinstance(next(all_source_reader.read(), None), Record)
