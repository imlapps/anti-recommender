from app.anti_recommendation_engine.anti_recommendation_engine import (
    AntiRecommendationEngine,
)
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)
from app.models.anti_recommendation import AntiRecommendation
from app.models.record import Record

import pytest
from pytest_mock import MockFixture


from app.readers.all_source_reader import AllSourceReader


def test_load_records(
    mocker: MockFixture,
    anti_recommendation_engine: AntiRecommendationEngine,
    records: tuple[Record, ...],
    records_by_key: tuple[dict[str, Record], ...],
) -> None:
    """Test that AntiRecommendationEngine.load_records() successfully reads in records for AntiRecommendationEngine's record store."""

    mocker.patch.object(AllSourceReader, "read", return_value=records)

    assert anti_recommendation_engine.load_records() == records_by_key


@pytest.mark.parametrize(
    "anti_recommender_type, AntiRecommender", [
        ("open_ai", OpenAiNormalAntiRecommender)]
)
def test_generate_anti_recommendations(
    anti_recommender_type: str,
    AntiRecommender: str,
    mocker: MockFixture,
    model_response: str,
    record_key: str,
    anti_recommendation_engine: AntiRecommendationEngine,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.generate_anti_recommendations yields AntiRecommendations of a given record key."""
    if anti_recommender_type == "open_ai":
        mocker.patch.object(
            AntiRecommender,
            "_generate_llm_response",
            return_value=model_response,
        )

    assert (
        next(anti_recommendation_engine.generate_anti_recommendations(record_key)).title
        == anti_recommendations[0].title
    )


def test_generate_initial_anti_recommendation_records(
    mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.generate_initial_anti_recommendation_records() returns a tuple of Records
    with keys that match the AntiRecommendations of the first Record in records."""

    mocker.patch.object(
        AntiRecommendationEngine,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    assert (
        anti_recommendation_engine_with_mocked_load_records.generate_initial_anti_recommendation_records()
        == records[1:]
    )


def test_generate_anti_recommendation_records(
    mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    record_key: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.generate_anti_recommendation_records() returns a tuple of Records
    with keys that match the AntiRecommendations of record_key.
    """

    mocker.patch.object(
        AntiRecommendationEngine,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    assert (
        anti_recommendation_engine_with_mocked_load_records.generate_anti_recommendation_records(
            record_key
        )
        == records[1:]
    )


def test_get_previous_anti_recommendation(
    mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    record_key: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.get_previous_anti_recommendation() returns a tuple containing records of previous anti-recommendations."""

    mocker.patch.object(
        AntiRecommendationEngine,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    anti_recommendation_engine_with_mocked_load_records.generate_initial_anti_recommendation_records()
    anti_recommendation_engine_with_mocked_load_records.generate_anti_recommendation_records(
        record_key
    )
    previous_anti_recommendation_records = (
        anti_recommendation_engine_with_mocked_load_records.get_previous_anti_recommendation_records()
    )

    if previous_anti_recommendation_records:
        assert previous_anti_recommendation_records[0] == records[0]


def test_get_previous_anti_recommendation_with_empty_stack(
    anti_recommendation_engine: AntiRecommendationEngine,
) -> None:
    """Test that AntiRecommendationEngine.get_previous_anti_recommendation() returns None when its stack is empty."""

    assert anti_recommendation_engine.get_previous_anti_recommendation_records() is None
