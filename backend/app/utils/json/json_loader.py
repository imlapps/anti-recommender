from app.utils.encodings.encodings_list import encodings_list
from app.utils.models.wikipedia_record import WikipediaRecord

from pathlib import Path
import json as json
import logging as logger
from typing import Tuple, Dict


def load_data(file_path: Path) -> Tuple[Dict, ...] | int:
    """Load and return documents from the JSON file."""
    wikipedia_data = {}

    try:
        json_list = (
            file_path.open(mode="r", encoding="utf-8").read().strip().split("\n")
        )
    except Exception:
        logger.warning("Invalid file path. Could not read in JSON data.")
        return 1

    for json_str in json_list:

        if "RECORD" in json_str:
            json_obj = ""
            for encoding in encodings_list:
                try:
                    json_obj = json.loads(bytes(json_str, encoding))
                    break
                except json.JSONDecodeError:
                    logger.warning(
                        "Invalid JSON format in the file. Could not read in JSON data."
                    )
                    return 1

            wikipedia_record = json_obj["record"]
            wikipedia_model = WikipediaRecord(**wikipedia_record)
            wikipedia_data[wikipedia_model.abstract_info.title] = wikipedia_model

    return tuple([wikipedia_data])
