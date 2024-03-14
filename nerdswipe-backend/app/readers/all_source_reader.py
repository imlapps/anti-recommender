
from collections.abc import Generator


from app.models.record.record import Record
from app.readers.reader.reader import Reader

from app.readers.readers_instantiator import ReadersInstantiator


class AllSourceReader:
    """A multiplexer for different Readers.

    Read in output data and yield them as Records.
    """

    def __init__(self) -> None:
        self.__readers: tuple[Reader, ...] | None = self.__get_readers()

    def __get_readers(self) -> tuple[Reader, ...] | None:
        """Get a tuple of Readers from ReadersInstantiator"""

        readers_instantiator = ReadersInstantiator()

        return readers_instantiator.provide_readers()

    def read(self) -> Generator[Record, None, None]:
        """Read in output data and yield Records."""
        for reader in self.__readers:
            yield from reader.read()
