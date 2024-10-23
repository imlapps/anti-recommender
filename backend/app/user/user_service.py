from abc import ABC, abstractmethod
from uuid import UUID

from app.models.anti_recommendations_selector import AntiRecommendationsSelector
from app.models.types import RecordKey


class UserService(ABC):
    @abstractmethod
    def add_to_user_anti_recommendations_history(
        self, *, user_id: UUID, anti_recommendation_key: RecordKey
    ) -> None:
        pass

    @abstractmethod
    def get_user_anti_recommendations_history(
        self, user_id: UUID
    ) -> tuple[RecordKey, ...]:
        pass

    @abstractmethod
    def get_user_last_seen_anti_recommendation(self, user_id: UUID) -> RecordKey:
        pass

    @abstractmethod
    def remove_slice_from_user_anti_recommendations_history(
        self,
        *,
        user_id: UUID,
        anti_recommendations_slice: AntiRecommendationsSelector.Slice
    ) -> None:
        pass
