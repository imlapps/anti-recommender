from enum import Enum


class AntiRecommendationsSelector(Enum):
    """An enum containing types used to select anti-recommendations from sequences."""

    LAST_TWO_RECORDS = "last two records"
