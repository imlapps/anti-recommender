from app.models.settings import settings
from app.readers.create_readers import create_readers
from app.readers.reader.wikipedia_reader import WikipediaReader


def test_create_readers() -> None:
    """Test that create_readers() returns the expected tuple of Readers,
    depending on the record_types in the environment variables."""

    assert isinstance(create_readers(settings)[0], WikipediaReader)
