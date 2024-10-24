from typing import NamedTuple


class AntiRecommendationsSelector:
    """A class containing `Slice` objects to match or select `AntiRecommendations` from sequences."""

    class Slice(NamedTuple):
        """
        A NamedTuple representing a slice of a sequence.

        The slice is within the interval: [start_index, end_index-1]

        If either of the indices are negative, it is relative to the end of the sequence.
        """

        start_index: int
        end_index: int

    SELECT_ALL_BUT_LAST_TWO_RECORDS = Slice(0, -2)
