from abc import ABC, abstractmethod 

class AntiRecommender(ABC):
    """
    An interface for the anti-recommendation engine
    """

    @abstractmethod 
    def generate_anti_recommendations(self) -> None:
        pass