from collections.abc import Iterable

from app.models import Record, settings
from app.readers.create_readers import create_readers
from app.readers.reader.reader import Reader


class AllSourceReader(Reader):
    """A multiplexer for different Readers.

    Read in output data and yield them as Records.
    """

    def __init__(self) -> None:
        self.__readers: tuple[Reader, ...] = create_readers(settings=settings)

    def read(self) -> Iterable[Record]:
        """Read in output data and yield Records."""
        for reader in self.__readers:
            yield from reader.read()
