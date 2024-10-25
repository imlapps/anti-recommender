from enum import Enum


class AntiRecommendationsSelector(str, Enum):

    REMOVE_LAST_TWO_RECORDS = "remove last two records"
