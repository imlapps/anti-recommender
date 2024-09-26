import pytest

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.models import Record
from app.models.types import RecordKey


@pytest.mark.order(1)
def test_get_previous_records_with_empty_stack(
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records returns an empty tuple when its stack is empty."""

    assert not anti_recommendation_engine.get_previous_records()


@pytest.mark.order(2)
def test_get_initial_records(
    records: tuple[Record, ...],
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_initial_records returns a tuple of Records
    with keys that match the AntiRecommendations of the first Record in records."""

    assert anti_recommendation_engine.get_initial_records() == records[1:]


@pytest.mark.order(3)
def test_get_next_records(
    records: tuple[Record, ...],
    record_key: RecordKey,
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_next_records returns a tuple of Records
    with keys that match the AntiRecommendations of record_key.
    """

    assert (
        anti_recommendation_engine.get_next_records(record_key=record_key)
        == records[1:]
    )


@pytest.mark.order(4)
def test_get_previous_records(
    records: tuple[Record, ...],
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records returns a tuple containing Records that match previous AntiRecommendations."""

    assert anti_recommendation_engine.get_previous_records()[0] == records[0]
