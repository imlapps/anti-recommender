from app.models.record import Record
from app.readers.all_source_reader import AllSourceReader


def test_read(all_source_reader: AllSourceReader) -> None:
    """Test that AllSourceReader.read() yields the expected output type."""

    assert isinstance(next(all_source_reader.read(), None), Record)
