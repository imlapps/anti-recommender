from abc import ABC, abstractmethod

from app.models.anti_recommendations_selector import AntiRecommendationsSelector
from app.models.types import RecordKey, UserId


class UserService(ABC):
    @abstractmethod
    def add_to_user_anti_recommendations_history(
        self, *, user_id: UserId, anti_recommendation_key: RecordKey
    ) -> None:
        pass

    @abstractmethod
    def get_user_anti_recommendations_history(
        self, user_id: UserId
    ) -> tuple[RecordKey, ...]:
        pass

    @abstractmethod
    def get_user_last_seen_anti_recommendation(self, user_id: UserId) -> RecordKey:
        pass

    @abstractmethod
    def remove_slice_from_user_anti_recommendations_history(
        self,
        *,
        user_id: UserId,
        anti_recommendations_slice: AntiRecommendationsSelector.Slice,
    ) -> None:
        pass
