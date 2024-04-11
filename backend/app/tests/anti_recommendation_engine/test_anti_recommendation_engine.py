import pytest
from pytest_mock import MockFixture

from app.anti_recommendation_engine.anti_recommendation_engine import (
    AntiRecommendationEngine,
)
from app.anti_recommenders.open_ai.normal_open_ai_anti_recommender import (
    NormalOpenAiAntiRecommender,
)
from app.models.record import Record
from app.models.settings import settings
from app.models.types import AntiRecommenderType, RecordType

ANTI_RECOMMENDER_TYPES = frozenset([AntiRecommenderType.OPEN_AI])


@pytest.fixture(autouse=True, params=ANTI_RECOMMENDER_TYPES, scope="module")
def _anti_recommender(
    request: pytest.FixtureRequest,
    session_mocker: MockFixture,
    model_response: str,
) -> None:
    """Mock AntiRecommenders based on parameterized types."""
    if request.param is AntiRecommenderType.OPEN_AI and settings.openai_api_key:
        session_mocker.patch.object(
            NormalOpenAiAntiRecommender,
            "_generate_llm_response",
            return_value=model_response,
        )


def test_get_previous_records_with_empty_stack(
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records() returns a tuple of None when its stack is empty."""

    assert anti_recommendation_engine.get_previous_records()[0] is None


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


def test_get_initial_records(
    records: tuple[Record, ...],
    record_type: RecordType,
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_initial_records() returns a tuple of Records
    with keys that match the AntiRecommendations of the first Record in records."""

    assert anti_recommendation_engine.get_initial_records(record_type) == records[1:]


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
