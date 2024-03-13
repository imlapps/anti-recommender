from app.models.record.record import Record
from app.readers.reader.wikipedia_reader import WikipediaReader


def test_read(wikipedia_reader: WikipediaReader) -> None:
    """Test that WikipediaReader.read() yields the expected output type."""

    assert isinstance(next(wikipedia_reader.read(), None), Record)
