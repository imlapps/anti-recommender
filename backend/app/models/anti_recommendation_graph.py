from typing import NamedTuple

from app.models import AntiRecommendation
from app.models.types import RecordKey


class AntiRecommendationGraph(NamedTuple):
    """
    A NamedTuple that contains the subject-objects relationship of an AntiRecommendation graph.

    `record_key` is the key of a Record, and the subject of the graph.

    `anti_recommendations` is a tuple of a Record's anti-recommendations, and the objects of the graph.
    """

    record_key: RecordKey
    anti_recommendations: tuple[AntiRecommendation, ...]
