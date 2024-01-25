from typing import Tuple, Dict
from app.utils.json import json_loader

class __Storage():
    """ 
    This class represents the main storage of all Wikipedia data in the NerdSwipe backend.
    It holds the Wikipedia output data, a stack containing Wikipedia records
    and the title of the current Wikipedia record.
    """
    def __init__(self) -> None:
        self.wikipedia_data = {}
        self.stack = []
        self.current_title = ""

    def read_wikipedia_data(self, file_path : str) -> None:
        """ Use the JSON Loader to read in the Wikpedia output data."""
        self.wikipedia_data = json_loader.load_data(file_path)[0]

    def add_title_to_stack(self, title : str) -> None:
        """ Add the title of a Wikipedia article to the stack."""
        self.stack.append(title)
    
    def pop_title_from_stack(self) -> str | None:
        """ 
        Remove an item from the from of the stack. 
        Return None if the stack is empty.
        """
        if len(self.stack) > 0:
            return self.stack.pop()
        
        return None
    
    def set_current_title(self, title : str = "", first_title : bool = False) -> None:    
        """Set the title of the current Wikipedia record."""

        # Use the first item in wikipedia_data
        if first_title and title == "":
            self.current_title = list(self.wikipedia_data.keys())[0]
        else:
            self.current_title = title 

    def get_current_title(self) -> str:
        """Return the title of the current Wikipedia record."""

        return self.current_title 

    def get_current_record(self) -> Tuple[Dict, ...]:
        """Return the record of the current Wikipedia record."""

        return tuple([{self.current_title : self.wikipedia_data.get(self.current_title, "")}])
    
    def get_article_records(self, article_title : str) -> Tuple[Dict,...] | None:
        """
        Return the Wikipedia record with a title that is same as article_title. 
        Return None if no such record exists.
        """
        if article_title in self.wikipedia_data:
            return tuple([{article_title : self.wikipedia_data[article_title]}])
        
        return None
    
    def reset(self) -> None:
        """
        Reset all variables in storage.
        """
        self.wikipedia_data = {}
        self.stack = []
        self.current_title = ""


storage = __Storage()

