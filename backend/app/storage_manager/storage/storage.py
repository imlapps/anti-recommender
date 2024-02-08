from typing import Tuple, Dict, List
from app.utils.json import json_loader


class Storage(object):
    """
    This class represents the main storage of all Wikipedia data in the NerdSwipe backend.
    It holds the Wikipedia output data, a stack containing Wikipedia records
    and the title of the current Wikipedia record.
    """

    def __init__(self) -> None:
        self.__wikipedia_data: Dict = {}
        self.__stack: List = []
        self.__current_title: str = ""

    def read_wikipedia_data(self, file_path: str) -> None:
        """Use the JSON Loader to read in the Wikpedia output data."""
        self.__wikipedia_data = json_loader.load_data(file_path)[0]

    def push_title_to_stack(self, title: str) -> None:
        """Add the title of a Wikipedia article to the stack."""
        self.__stack.append(title)

    def pop_title_from_stack(self) -> str | None:
        """
        Remove an item from the from of the stack.
        Return None if the stack is empty.
        """
        if len(self.__stack) > 0:
            return self.__stack.pop()

        return None

    def set_current_title_to_first_item_title(self) -> None:
        """Use the title of the first item in __wikipedia_data as the current_title"""
        if self.__wikipedia_data:
            self.__current_title = list(self.__wikipedia_data.keys())[0]

    @property
    def current_title(self) -> str:
        """Return the title of the current Wikipedia record."""

        return self.__current_title

    @current_title.setter
    def current_title(self, title: str = "") -> None:
        """Set the title of the current Wikipedia record."""

        # Use the first item in wikipedia_data

        self.__current_title = title

    def get_current_record(self) -> Tuple[Dict, ...]:
        """Return the record of the current Wikipedia record."""

        return tuple(
            [
                {
                    self.__current_title: self.__wikipedia_data.get(
                        self.__current_title, ""
                    )
                }
            ]
        )

    def get_article_records(self, article_title: str) -> Tuple[Dict, ...] | None:
        """
        Return the Wikipedia record with a title that is same as article_title.
        Return None if no such record exists.
        """
        if article_title in self.__wikipedia_data:
            return tuple([{article_title: self.__wikipedia_data[article_title]}])

        return None

    def reset(self) -> None:
        """
        Reset all variables in storage.
        """
        self.__wikipedia_data = {}
        self.__stack = []
        self.__current_title = ""
