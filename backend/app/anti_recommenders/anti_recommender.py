from abc import ABC, abstractmethod
from collections.abc import Iterator

from app.models.anti_recommendation import AntiRecommendation
from app.models.types import RecordType


class AntiRecommender(ABC):
    """
    An interface to generate AntiRecommendations of a record.
    """

    @abstractmethod
    def generate_anti_recommendations(
        self, record_key: str, record_type: str
    ) -> Iterator[AntiRecommendation, None, None]:
        pass
