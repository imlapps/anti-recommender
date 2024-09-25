from typing import NamedTuple

from app.models import AntiRecommendation
from app.models.types import RecordKey


class AntiRecommendationGraph(NamedTuple):
    """
    A NamedTuple that contains the subject-object relationship of an AntiRecommendation graph.

    An AntiRecommendationGraph consists of:

    `record_key` - The key of a Record, and the subject of the graph.

    `anti_recommendations` - A tuple of a Record's anti-recommendations, and the objects of the graph.
    """

    record_key: RecordKey
    anti_recommendations: tuple[AntiRecommendation, ...]
