from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.models.anti_recommendation import AntiRecommendation
from app.models.types import RecordKey


class AntiRecommender(ABC):
    """
    An interface to generate AntiRecommendations of a record.
    """

    @abstractmethod
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        pass
