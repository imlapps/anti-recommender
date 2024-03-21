import pytest
from pytest_mock import MockFixture

from app.anti_recommendation_engine.anti_recommendation_engine import (
    AntiRecommendationEngine,
)
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)
from app.models.anti_recommendation import AntiRecommendation
from app.models.record import Record
from app.readers.all_source_reader import AllSourceReader


def test_load_records(
    session_mocker: MockFixture,
    anti_recommendation_engine: AntiRecommendationEngine,
    records: tuple[Record, ...],
    records_by_key: tuple[dict[str, Record], ...],
) -> None:
    """Test that AntiRecommendationEngine.load_records() successfully reads in Records for AntiRecommendationEngine's records_by_key."""

    session_mocker.patch.object(AllSourceReader, "read", return_value=records)

    assert anti_recommendation_engine.load_records() == records_by_key


@pytest.mark.parametrize(
    ("anti_recommender_type", "anti_recommender"),
    [("open_ai", OpenAiNormalAntiRecommender)],
)
def test_generate_anti_recommendations(  # noqa: PLR0913
    record_key: str,
    session_mocker: MockFixture,
    model_response: str,
    anti_recommender: str,
    anti_recommender_type: str,
    anti_recommendation_engine: AntiRecommendationEngine,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.generate_anti_recommendations() yields AntiRecommendations of a given record key."""
    if anti_recommender_type == "open_ai":
        session_mocker.patch.object(
            anti_recommender,
            "_generate_llm_response",
            return_value=model_response,
        )

    assert (
        next(anti_recommendation_engine.generate_anti_recommendations(record_key)).title
        == anti_recommendations[0].title
    )


def test_get_initial_records_of_anti_recommendations(
    session_mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.get_initial_records_of_anti_recommendations() returns a tuple of Records
    with keys that match the AntiRecommendations of the first Record in records."""

    session_mocker.patch.object(
        AntiRecommendationEngine,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    assert (
        anti_recommendation_engine_with_mocked_load_records.get_initial_records_of_anti_recommendations()
        == records[1:]
    )


def test_get_records_of_anti_recommendations(
    session_mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    record_key: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.get_records_of_anti_recommendations() returns a tuple of Records
    with keys that match the AntiRecommendations of record_key.
    """

    session_mocker.patch.object(
        AntiRecommendationEngine,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    assert (
        anti_recommendation_engine_with_mocked_load_records.get_records_of_anti_recommendations(
            record_key
        )
        == records[1:]
    )


def test_get_previous_records_of_anti_recommendations(
    session_mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    record_key: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records_of_anti_recommendations() returns a tuple containing Records of previous AntiRecommendations."""

    session_mocker.patch.object(
        AntiRecommendationEngine,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    anti_recommendation_engine_with_mocked_load_records.get_initial_records_of_anti_recommendations()
    anti_recommendation_engine_with_mocked_load_records.get_records_of_anti_recommendations(
        record_key
    )
    previous_anti_recommendation_records = (
        anti_recommendation_engine_with_mocked_load_records.get_previous_records_of_anti_recommendations()
    )

    if previous_anti_recommendation_records:
        assert previous_anti_recommendation_records[0] == records[0]


def test_get_previous_records_of_anti_recommendations_with_empty_stack(
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_records_of_anti_recommendations() returns a tuple of None when its stack is empty."""

    assert (
        anti_recommendation_engine.get_previous_records_of_anti_recommendations()[0]
        is None
    )
