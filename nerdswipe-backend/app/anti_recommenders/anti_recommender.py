from abc import ABC, abstractmethod
from collections.abc import Generator

from app.models.anti_recommendation.anti_recommendation import AntiRecommendation


__all__ = ["AntiRecommender"]


class AntiRecommender(ABC):
    """
    An interface to generate anti-recommendations of a record.
    """

    @abstractmethod
    def generate_anti_recommendations(
        self, record_key: str
    ) -> Generator[AntiRecommendation, None, None]:
        pass
