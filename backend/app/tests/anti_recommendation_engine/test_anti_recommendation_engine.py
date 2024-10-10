import pytest
from pytest_mock import MockFixture

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.models import Record, UserState
from app.models.types import RecordKey


@pytest.mark.order(1)
def test_get_previous_records_with_empty_stack(
    anti_recommendation_engine: AntiRecommendationEngine, user_state: UserState
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records returns an empty tuple when its stack is empty."""

    anti_recommendation_engine.initialize_anti_recommender(user_state=user_state)
    assert not anti_recommendation_engine.previous_records()


@pytest.mark.order(2)
def test_get_initial_records(
    records: tuple[Record, ...],
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_initial_records returns a tuple of Records
    with keys that match the AntiRecommendations of the first Record in records."""

    assert anti_recommendation_engine.initial_records() == records[1:]


@pytest.mark.order(3)
def test_get_next_records(
    records: tuple[Record, ...],
    record_key: RecordKey,
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_next_records returns a tuple of Records
    with keys that match the AntiRecommendations of record_key.
    """

    assert anti_recommendation_engine.next_records(record_key=record_key) == records[1:]


@pytest.mark.order(4)
def test_get_previous_records(
    records: tuple[Record, ...],
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records returns a tuple containing Records that match previous AntiRecommendations."""

    assert anti_recommendation_engine.previous_records()[0] == records[0]


@pytest.mark.order(5)
def test_initialize_anti_recommender(
    anti_recommendation_engine: AntiRecommendationEngine,
    session_mocker: MockFixture,
    user_state: UserState,
) -> None:
    """Test that AntiRecommendationEngine.initialize_anti_recommender instantiates an AntiRecommender internally."""

    mock_anti_recommendation_engine__select_anti_recommender = (
        session_mocker.patch.object(
            AntiRecommendationEngine, "select_anti_recommender", return_value=None
        )
    )

    anti_recommendation_engine.initialize_anti_recommender(user_state=user_state)

    mock_anti_recommendation_engine__select_anti_recommender.assert_called()
