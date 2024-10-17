from enum import Enum


class AntiRecommenderType(str, Enum):
    """An enum of anti-recommender types."""

    OPEN_AI = "OpenAI"
    ARKG = "ARKG"
