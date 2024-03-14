from app.models.settings.settings import settings
from app.readers.reader.reader import Reader
from app.readers.reader.wikipedia_reader import WikipediaReader


class ReadersInitializer:
    """
    An initializer for the different Readers.
    """

    def __init__(self):
        self.__record_types: frozenset[str] | None = self.__retrieve_record_types(
        )

    def __retrieve_record_types(self) -> frozenset[str] | None:
        if settings.record_types:
            return settings.record_types
        return None

    def provide_readers(self) -> tuple[Reader, ...] | None:

        if self.__record_types:
            readers = []

            for record_type in self.__retrieve_record_types():
                if record_type.lower() == "wikipedia":
                    readers.append(WikipediaReader)

            if readers:
                return tuple(readers)

        return None
