from pathlib import Path
from collections.abc import Generator

from app.utils.config.config import config
from app.models.record.record import Record
from app.readers.reader.wikipedia_reader.wikipedia_reader import WikipediaReader


class AllSourceReader:
    """A multiplexor of different Readers.

    Read in output data and yield them as Records.
    """

    def __init__(self) -> None:
        self.__record_type: str | None = self.__get_record_type()
        self.__file_output_path: Path | None = self.__get_output_path()

    def __get_record_type(self) -> str | None:
        """Retrieve the record type from environment variables."""

        return config[0].get("RECORD_TYPE", None)

    def __get_output_path(self) -> Path | None:
        """Retrieve record output path from environment variables."""

        if self.__record_type:
            file_name = config[0].get(
                self.__record_type.upper() + "_OUTPUT_FILE_NAME", None
            )
            if file_name:
                return Path(__file__).parent.parent / "data" / file_name

        return None

    def read(self) -> Generator[Record, None, None]:
        """Read in output data and yield Records."""
        if self.__file_output_path:
            if self.__record_type == "Wikipedia":
                reader = WikipediaReader(self.__file_output_path)

            yield from reader.read()
