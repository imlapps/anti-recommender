from collections.abc import Generator
from app.models.settings.settings import config

from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.anti_recommenders.anti_recommender import AntiRecommender


class AntiRecommenderProxy:
    """
    A multiplexer for different anti-recommenders.
    """

    def __init__(self) -> None:
        self.__type: str | None = self.__get_anti_recommender_type()
        self.__anti_recommender: AntiRecommender | None = None

    def __get_anti_recommender_type(self) -> str | None:
        """Retrieve Anti-Recommender type from environment variables."""

        return config[0].get("ANTI_RECOMMENDER_TYPE", None)

    def generate_anti_recommendations(
        self, record_key: str
    ) -> Generator[AntiRecommendation, None, None]:
        """Yield anti-recommendations of a given record key."""

        if self.__type == "OPENAI" and config[0].get("OPENAI_API_KEY", None):
            self.__anti_recommender = OpenAiNormalAntiRecommender()
            yield from self.__anti_recommender.generate_anti_recommendations(record_key)
