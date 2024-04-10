from collections.abc import Iterator

from app.models.record import Record
from app.models.settings import settings
from app.readers.reader.reader import Reader
from app.readers.create_readers import create_readers


class AllSourceReader(Reader):
    """A multiplexer for different Readers.

    Read in output data and yield them as Records.
    """

    def __init__(self) -> None:
        self.__readers: tuple[Reader, ...] = create_readers(settings=settings)

    def read(self) -> Iterator[Record, None, None]:
        """Read in output data and yield Records."""
        for reader in self.__readers:
            if reader:
                yield from reader.read()
