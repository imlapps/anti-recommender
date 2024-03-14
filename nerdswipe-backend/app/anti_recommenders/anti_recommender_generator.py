
from collections.abc import Generator
from app.models.settings.settings import settings

from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)


from app.anti_recommenders.anti_recommender import AntiRecommender


class AntiRecommendationGenerator(AntiRecommender):
    """
    A generator of AntiRecommendations.
    An AntiRecommender is selected based on values stored in settings.
    """

    def __init__(self) -> None:
        self.__type: str | None = settings.anti_recommender_type
        self.__anti_recommender: AntiRecommender | None = None

    def generate_anti_recommendations(
        self, record_key: str
    ) -> Generator[AntiRecommendation, None, None]:
        """Yield anti-recommendations of a given record key."""

        if self.__type.lower() == "openai":
            if settings.openai_api_key:
                self.__anti_recommender = OpenAiNormalAntiRecommender()
            yield from self.__anti_recommender.generate_anti_recommendations(record_key)
