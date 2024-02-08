from pathlib import Path
from typing import Tuple, Dict
from fastapi import Depends
from typing_extensions import Annotated

from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy
from app.storage_manager.storage.storage import Storage

__all__ = ["StorageManager"]


class StorageManager(object):
    """
    This class serves as the main access point of Wikipedia storage and handles all operations
    related to the storage of Wikipedia data in NerdSwipe backend. It holds a Storage object and
    the output path for the Wikipedia output data.
    """

    def __init__(self, storage: Storage, wikipedia_output_path) -> None:
        self.__wikipedia_storage = storage
        self.__wikipedia_output_path = wikipedia_output_path

    def initialize_wikipedia_data(self) -> None:
        """Read Wikipedia data into __wikipedia_storage and set the current title in __wikipedia_storage"""
        self.__wikipedia_storage.read_wikipedia_data(self.__wikipedia_output_path)
        self.__wikipedia_storage.set_current_title_to_first_item_title()

    def __retrieve_anti_recommendations_in_storage(
        self, anti_recommendations: Tuple[Tuple[str, ...], ...]
    ) -> Tuple[Dict, ...]:
        wikipedia_articles = []
        """Return a tuple of Wikipedia records that are present in the tuple of anti-recommendations and can be found in __wikipedia_storage"""

        # This loop retrieves the records of the anti-recommendations, if they exist in storage
        # Each article is a tuple of the form: (wikipedia_title, wikipedia_url)
        for article in anti_recommendations:
            article_record = self.__wikipedia_storage.get_article_records(article[0])

            if article_record is not None:
                wikipedia_articles.append(article_record[0])

        if len(wikipedia_articles) == 0:
            wikipedia_articles.append({})

        # Add the current title to the stack. This is now the previous article in storage.
        self.__wikipedia_storage.push_title_to_stack(
            self.__wikipedia_storage.current_title
        )

        # Set the first item in wikipedia_articles as the new current title in storage.
        current_title = ""

        if wikipedia_articles[0]:
            current_title = list(wikipedia_articles[0].keys())[0]

        self.__wikipedia_storage.current_title = current_title

        # return a tuple of Wikipedia articles
        return tuple(wikipedia_articles)

    def retrieve_current_wikipedia_article(self) -> Tuple[Dict, ...]:
        """
        This method retrieves the previous Wikipedia article from storage and returns it.
        """

        return self.__wikipedia_storage.get_current_record()

    def retrieve_next_wikipedia_articles(
        self, anti_recommender: Annotated[AntiRecommenderProxy, Depends()]
    ) -> Tuple[Dict, ...]:
        """
        This method returns a tuple that contains an article's anti-recommendation records.
        An empty tuple (with an empty dict) is returned if no anti-recommendations are obtained.
        """

        # Set the title of the anti-recommender engine
        # If no title is given, use the current title in storage
        if anti_recommender.title == "":
            anti_recommender.title = self.__wikipedia_storage.current_title

        # return a tuple of anti-recommendations that are present in storage.
        return tuple(
            [
                {
                    "anti_recommendations": self.__retrieve_anti_recommendations_in_storage(
                        anti_recommender.generate_anti_recommendations()
                    )
                }
            ]
        )

    def retrieve_previous_wikipedia_article(self) -> Tuple[Dict, ...]:
        """
        This method retrieves the previous Wikipedia article from storage.
        """

        self.__wikipedia_storage.current_title = (
            self.__wikipedia_storage.pop_title_from_stack()
        )

        return self.__wikipedia_storage.get_current_record()

    def reset_storage_manager(self) -> None:
        """
        Reset all variables in the StorageManager.
        """
        self.__wikipedia_storage.reset()
        self.__wikipedia_output_path = Path()
