from app.readers.readers_instantiator import ReadersInstantiator
from app.readers.reader.wikipedia_reader import WikipediaReader


def test_provide_readers() -> None:
    """Test that ReadersInitializer.provide_readers() returns the expected tuple of Readers,
    depending on the record_types in the environment variables."""

    readers_instantiator = ReadersInstantiator()

    assert isinstance(readers_instantiator.provide_readers()
                      [0], WikipediaReader)
