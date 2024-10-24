import json
from collections.abc import Iterable
from pathlib import Path

from unidecode import unidecode

from app.models import wikipedia
from app.readers.reader import Reader


class WikipediaReader(Reader):
    """A concrete implementation of Reader.

    Read in Wikipedia output data and yield them as Articles.
    """

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

    def read(self) -> Iterable[wikipedia.Article]:
        """Read in Wikipedia output data and yield Records."""

        with self.__file_path.open(encoding="utf-8") as json_file:
            for json_line in json_file:
                record_json = json.loads(json_line)

                if record_json["type"] != "RECORD":
                    continue

                json_obj = json.loads(
                    unidecode(json.dumps(record_json["record"], ensure_ascii=False))
                )

                yield wikipedia.Article(**(json_obj["abstract_info"]), **(json_obj))
