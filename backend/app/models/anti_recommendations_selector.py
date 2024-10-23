from typing import NamedTuple


class AntiRecommendationsSelector:

    class Slice(NamedTuple):
        start_index: int
        end_index: int

    SELECT_ALL_BUT_LAST_TWO_RECORDS = Slice(0, -2)
