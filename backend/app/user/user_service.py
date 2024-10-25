from abc import ABC, abstractmethod

from app.models.anti_recommendations_selector import AntiRecommendationsSelector
from app.models.types import RecordKey, UserId


class UserService(ABC):
    """An interface to manage the state of a `User`."""

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
    def get_user_last_seen_anti_recommendation(
        self, user_id: UserId
    ) -> RecordKey | None:
        pass

    @abstractmethod
    def remove_anti_recommendations_from_user_history(
        self,
        *,
        user_id: UserId,
        selector: AntiRecommendationsSelector,
    ) -> None:
        pass
