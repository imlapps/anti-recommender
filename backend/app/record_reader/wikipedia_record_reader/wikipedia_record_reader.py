from __future__ import annotations

import json
import logging as logger
from typing import TYPE_CHECKING

from ..record_reader import RecordReader
from app.utils.encodings.encodings_list import encodings
from app.utils.models.wikipedia_record import WikipediaRecord

if TYPE_CHECKING:
    from pathlib import Path


class WikipediaRecordReader(RecordReader):
    """A concrete implementation of RecordReader.

    Read in different formats of data and parse them into Wikipedia records.
    """

    def load_json_data(
        self: WikipediaRecordReader,
        file_path: Path,
    ) -> tuple[dict, ...] | int:
        """Load and return Wikipedia records from a JSON file."""
        wikipedia_data = {}

        if not file_path.exists():
            logger.warning(
                "Could not read in JSON data. File path does not exist.")
            return 1

        json_list = (
            file_path.open(
                mode="r", encoding="utf-8").read().strip().split("\n")
        )

        for json_str in json_list:

            if "RECORD" in json_str:
                json_obj = {}
                for encoding in encodings:
                    json_obj = json.loads(bytes(json_str, encoding))
                    break

                wikipedia_model = WikipediaRecord(**(json_obj["record"]))
                wikipedia_data[wikipedia_model.abstract_info.title] = wikipedia_model

        return tuple([wikipedia_data])
