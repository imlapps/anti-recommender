import json
from pathlib import Path
from unidecode import unidecode
from collections.abc import Iterator


from app.models.wikipedia.article import Article
from app.readers.reader.reader import Reader


class WikipediaReader(Reader):
    """A concrete implementation of Reader.

    Read in Wikipedia output data and yield them as WikipediaArticles.
    """

    def __init__(self, file_path: Path) -> None:
        self.__file_path = file_path

    def read(self) -> Iterator[Article, None, None]:
        """Read in Wikipedia output data and yield Records."""

        with self.__file_path.open(mode="r", encoding="utf-8") as json_file:

            for json_line in json_file:
                record_json = json.loads(json_line)

                if record_json["type"] != "RECORD":
                    continue

                json_obj = json.loads(
                    unidecode(json.dumps(
                        record_json["record"], ensure_ascii=False))
                )

                yield Article(**(json_obj["abstract_info"]), **(json_obj))
