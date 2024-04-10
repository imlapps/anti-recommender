from abc import ABC, abstractmethod
from collections.abc import Iterator

from app.models.anti_recommendation import AntiRecommendation


class AntiRecommender(ABC):
    """
    An interface to generate AntiRecommendations of a record.
    """

    @abstractmethod
    def generate_anti_recommendations(
        self, record_key: str
    ) -> Iterator[AntiRecommendation, None, None]:
        pass
