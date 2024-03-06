import os

from dotenv import load_dotenv
from pathlib import Path
from collections.abc import Generator

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

        load_dotenv()

        return os.getenv("RECORD_TYPE")

    def __get_output_path(self) -> Path | None:
        """Retrieve record output path from environment variables."""

        load_dotenv()

        if self.__record_type:
            return Path(__file__).parent.parent / "data" / os.getenv(self.__record_type.capitalize() + "_OUTPUT_FILE_NAME")

        return None

    def read(self) -> Generator[Record, None, None]:
        """ Read in output data and yield Records."""
        if self.__file_output_path:
            if self.__record_type == "Wikipedia":
                reader = WikipediaReader(
                    file_path=self.__file_output_path)

            yield from reader.read()
