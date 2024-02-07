import os
from typing import Tuple
from .anti_recommender import AntiRecommender
from .open_ai.regular_open_ai_anti_recommender import RegularOpenAiAntiRecommender


class AntiRecommenderProxy(AntiRecommender):
    """
    The Proxy class for the anti-recommendation engine.
    """

    def __init__(self, wikipedia_title: str = "", type: str = "openai"):
        self.__wikipedia_title = wikipedia_title
        self.__anti_recommender = None
        self.__type = type

    @property
    def title(self) -> str:
        """return the title of the Wikipedia article."""

        return self.__wikipedia_title

    @title.setter
    def title(self, title) -> None:
        """store the title of the Wikipedia article."""

        self.__wikipedia_title = title

    def generate_anti_recommendations(self) -> Tuple[Tuple[str, ...], ...]:
        """Generate anti-recommendations"""

        if self.__type == "openai":
            if "OPENAI_API_KEY" in os.environ:
                self.__anti_recommender = RegularOpenAiAntiRecommender()

        return self.__anti_recommender.generate_anti_recommendations(
            self.__wikipedia_title
        )
