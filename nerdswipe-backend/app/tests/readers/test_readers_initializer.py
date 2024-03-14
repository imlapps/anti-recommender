from app.readers.reader.wikipedia_reader import WikipediaReader

from app.readers.readers_initializer import ReadersInitializer


def test_provide_readers() -> None:
    """Test that ReadersInitializer.provide_readers() returns the expected tuple of Readers,
    depending on the record_types in the environment variables."""

    readers_initializer = ReadersInitializer()

    assert readers_initializer.provide_readers() == tuple([WikipediaReader])
