import json
from pathlib import Path
from collections.abc import Generator

from app.models.record import Record
from app.readers.reader.reader import Reader
from app.utils.encodings.encodings_list import encodings


class WikipediaReader(Reader):
    """A concrete implementation of Reader.

    Read in Wikipedia output data and yield them as Records.
    """

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

    def read(self) -> Generator[Record, None, None]:
        """Read in Wikipedia output data and yield Records."""

        json_list = (
            self.__file_path.open(
                mode="r", encoding="utf-8").read().strip().split("\n")
        )

        for json_str in json_list:

            if "RECORD" in json_str:
                json_obj = {}
                for encoding in encodings:
                    json_obj = json.loads(bytes(json_str, encoding))
                    break

                wikipedia_record = Record(**(json_obj["record"]))
                yield wikipedia_record
