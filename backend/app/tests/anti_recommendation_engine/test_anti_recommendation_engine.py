import pytest
from app.models.settings import settings
from app.anti_recommendation_engine.anti_recommendation_engine import (
    AntiRecommendationEngine,
)
from app.models.record import Record
from app.models.types import RecordType


def test_get_previous_records_with_empty_stack(
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records() returns a tuple of None when its stack is empty."""

    assert anti_recommendation_engine.get_previous_records()[0] is None


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_get_previous_records(
    records: tuple[Record, ...],
    record_key: str,
    record_type: RecordType,
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records() returns a tuple containing Records that match previous AntiRecommendations."""

    anti_recommendation_engine.get_initial_records(record_type)
    anti_recommendation_engine.get_next_records(record_key, record_type)

    assert anti_recommendation_engine.get_previous_records()[0] == records[0]


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_get_initial_records(
    records: tuple[Record, ...],
    record_type: RecordType,
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_initial_records() returns a tuple of Records
    with keys that match the AntiRecommendations of the first Record in records."""

    assert anti_recommendation_engine.get_initial_records(
        record_type) == records[1:]


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_get_next_records(
    records: tuple[Record, ...],
    record_key: str,
    record_type: RecordType,
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_next_records() returns a tuple of Records
    with keys that match the AntiRecommendations of record_key.
    """

    assert (
        anti_recommendation_engine.get_next_records(record_key, record_type)
        == records[1:]
    )
