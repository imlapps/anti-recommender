from pathlib import Path
from app.models.settings.settings import settings
from app.readers.reader.reader import Reader
from app.readers.reader.wikipedia_reader import WikipediaReader


class ReadersInstantiator:
    """
    An Instantiator for the different Readers.
    """

    def __init__(self):
        self.__record_types: frozenset[str] | None = self.__retrieve_record_types(
        )
        self.__file_output_paths: list[Path] | None = self.__get_output_paths()

    def __retrieve_record_types(self) -> frozenset[str] | None:
        """Retrieve a frozenset of record types from settings."""

        if settings.record_types:
            return settings.record_types
        return None

    def __get_output_paths(self) -> list[Path] | None:
        """Retrieve output file names from settings and return a list of file output paths."""

        return [
            Path(__file__).parent.parent / "data" / file_name
            for file_name in settings.output_file_names
        ]

    def provide_readers(self) -> tuple[Reader, ...] | None:
        """Return a tuple of Readers depending on the record type obtained from settings. 
           Readers are instantiated with Paths that contain the corresponding record types in the Path names.
        """
        if self.__record_types:
            readers = []

            for record_type in self.__retrieve_record_types():
                if record_type.lower() == "wikipedia":
                    readers.extend(
                        [
                            WikipediaReader(file_output_path)
                            for file_output_path in self.__file_output_paths
                            if record_type.lower() in str(file_output_path)
                        ]
                    )

            if readers:
                return tuple(readers)

        return None
