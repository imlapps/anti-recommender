import os
from typing import Tuple 
from .anti_recommender import AntiRecommender
from .open_ai.regular_open_ai_anti_recommender import RegularOpenAIAntiRecommender

class AntiRecommenderProxy(AntiRecommender):
    """
    The Proxy class for the anti-recommendation engine.
    """

    def __init__(self, wikipedia_title: str = None):
        self.wikipedia_title : str = wikipedia_title
        self.anti_recommender = None

    def set_title(self, title:str) -> None:
        """store the title of the Wikipedia article."""

        self.wikipedia_title = title 

    def get_title(self) -> str | None:
        """return the title of the Wikipedia article."""
        
        return self.wikipedia_title 
    
    def generate_anti_recommendations(self, type: str = "openai") -> Tuple[Tuple, ...]:
        """Generate anti-recommendations"""

        if type == "openai":
            if 'OPENAI_API_KEY' in os.environ:
                self.anti_recommender  = RegularOpenAIAntiRecommender()

        return self.anti_recommender.generate_anti_recommendations(self.wikipedia_title)
