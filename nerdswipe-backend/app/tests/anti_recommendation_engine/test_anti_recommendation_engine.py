from app.anti_recommendation_engine.anti_recommendation_engine import (
    AntiRecommendationEngine,
)
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from app.models.record.record import Record
from pytest_mock import MockFixture

from app.anti_recommenders.anti_recommender_generator import AntiRecommendationGenerator
from app.readers.all_source_reader import AllSourceReader


def test_load_records(
    mocker: MockFixture,
    anti_recommendation_engine: AntiRecommendationEngine,
    records: tuple[Record, ...],
    record_store: tuple[dict[str, Record], ...],
) -> None:
    """Test that AntiRecommendationEngine.load_records() successfully reads in records for AntiRecommendationEngine's record store."""

    mocker.patch.object(AllSourceReader, "read", return_value=records)

    assert anti_recommendation_engine.load_records() == record_store


def test_generate_anti_recommendation_records_with_no_record_key_passed(
    mocker: MockFixture,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.generate_anti_recommendations() returns a tuple containing records of anti-recommendations."""

    mocker.patch.object(
        AntiRecommendationGenerator,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    assert (
        anti_recommendation_engine_with_mocked_load_records.generate_anti_recommendation_records()
        == records[1:]
    )


def test_generate_anti_recommendation_records_with_record_key_passed(
    mocker: MockFixture,
    record_key: str,
    anti_recommendation_engine_with_mocked_load_records: AntiRecommendationEngine,
    records: tuple[Record, ...],
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that AntiRecommendationEngine.generate_anti_recommendations() returns a tuple containing records of anti-recommendations."""

    mocker.patch.object(
        AntiRecommendationGenerator,
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
        AntiRecommendationGenerator,
        "generate_anti_recommendations",
        return_value=anti_recommendations,
    )

    anti_recommendation_engine_with_mocked_load_records.generate_anti_recommendation_records()
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
