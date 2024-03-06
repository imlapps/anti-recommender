import os
from typing import Generator
from app.anti_recommender.anti_recommender import AntiRecommender
from dotenv import load_dotenv

from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from app.anti_recommender.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import OpenAiNormalAntiRecommender


class AntiRecommenderProxy:
    def __init__(self) -> None:
        self.__type: str | None = self.__get_anti_recommender_type()
        self.__anti_recommender: AntiRecommender | None = None

    def __get_anti_recommender_type(self) -> str | None:
        """ Retrieve Anti-Recommender type from environment variables."""

        load_dotenv()

        return os.getenv("ANTI_RECOMMENDER_TYPE")

    def generate_anti_recommendations(self, record_key: str) -> Generator[AntiRecommendation, None, None]:
        """ Yield anti-recommendations of a given record key."""

        load_dotenv()

        if self.__type == "OPENAI":
            if os.getenv("OPENAI_API_KEY"):
                self.__anti_recommender = OpenAiNormalAntiRecommender()
                yield from self.__anti_recommender.generate_anti_recommendations(record_key)
