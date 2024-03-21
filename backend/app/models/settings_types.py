from enum import Enum


class AntiRecommenderType(str, Enum):
    """An enum of anti-recommender types."""

    open_ai = "OpenAI"


class RecordType(str, Enum):
    """An enum of record types."""

    wikipedia = "Wikipedia"
