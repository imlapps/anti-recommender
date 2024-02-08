from typing import Tuple
from abc import ABC, abstractmethod

__all__ = ["AntiRecommender"]


class AntiRecommender(ABC):
    """
    An interface for the anti-recommendation engine
    """

    @abstractmethod
    def generate_anti_recommendations(self) -> Tuple[Tuple, ...]:
        pass
