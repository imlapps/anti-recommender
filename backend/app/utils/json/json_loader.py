from app.utils.encodings.encodings_list import encodings_list
from app.utils.models.wikipedia_record import WikipediaRecord


import json as json
import pathlib as Path
from typing import Tuple, Dict 


def load_data(file_path: Path) -> Tuple[Dict, ...]:
        """Load and return documents from the JSON file."""
        wikipedia_data = {}
        
        with  file_path.open(mode = "r", encoding = "utf-8") as json_file:
            json_list = json_file.read().strip().split("\n")
            for json_str in json_list:

                if "RECORD" in json_str:
                    json_obj = ""
                    for encoding in encodings_list:
                        try:
                            json_obj = json.loads(bytes(json_str, encoding))
                            break
                        except json.JSONDecodeError:
                            print("Error: Invalid JSON format in the file.")
                        
                    wikipedia_record = json_obj["record"]
                    wikipedia_model = WikipediaRecord(**wikipedia_record)
                    wikipedia_data[wikipedia_model.abstract_info.title] = wikipedia_model
                    
        return tuple([wikipedia_data])
