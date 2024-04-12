from app.models import wikipedia
from app.readers.reader.wikipedia_reader import WikipediaReader


def test_read(wikipedia_reader: WikipediaReader) -> None:
    """Test that WikipediaReader.read() yields the expected output type."""

    assert isinstance(next(iter(wikipedia_reader.read())), wikipedia.Article)
