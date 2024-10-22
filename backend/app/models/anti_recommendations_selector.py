from enum import Enum


class AntiRecommendationsSelector(tuple, Enum):
    SELECT_ALL_BUT_LAST_TWO = (0, -2)
