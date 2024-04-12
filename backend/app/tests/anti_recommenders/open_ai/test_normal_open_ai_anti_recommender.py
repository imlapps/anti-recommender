import pytest
from langchain.schema.runnable import RunnableSequence, RunnableSerializable
from pytest_mock import MockFixture

from app.anti_recommenders.open_ai.normal_open_ai_anti_recommender import (
    NormalOpenAiAntiRecommender,
)
from app.models.anti_recommendation import AntiRecommendation
from app.models.settings import settings
from app.models.types.record_type import RecordType


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_build_chain(
    open_ai_normal_anti_recommender: NormalOpenAiAntiRecommender,
) -> None:
    """Test that OpenAiNormalAntiRecommender._build_chain() returns an OpenAI chain of type RunnableSerializable."""

    assert isinstance(
        open_ai_normal_anti_recommender._build_chain(),  # noqa: SLF001
        RunnableSerializable,
    )


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_create_query(
    open_ai_normal_anti_recommender: NormalOpenAiAntiRecommender,
    record_key: str,
    record_type: RecordType,
) -> None:
    """Test that OpenAiNormalAntiRecommender._create_query() returns an OpenAI query when passed a record key."""

    assert record_key in open_ai_normal_anti_recommender._create_query(  # noqa: SLF001
        record_key, record_type
    )


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_generate_llm_response(
    session_mocker: MockFixture,
    open_ai_normal_anti_recommender: NormalOpenAiAntiRecommender,
    model_response: str,
    record_key: str,
    record_type: RecordType,
) -> None:
    """Test that OpenAiNormalAntiRecommender._generate_llm_response() returns a response from an OpenAI large language model."""

    # Mock RunnableSerializable's invoke method and return an LLM response
    session_mocker.patch.object(
        RunnableSequence,
        "invoke",
        return_value=model_response,
    )

    assert (
        open_ai_normal_anti_recommender._generate_llm_response(  # noqa: SLF001
            open_ai_normal_anti_recommender._create_query(  # noqa: SLF001
                record_key, record_type
            ),
            open_ai_normal_anti_recommender._build_chain(),  # noqa: SLF001
        )
        == model_response
    )


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_parse_llm_response(
    open_ai_normal_anti_recommender: NormalOpenAiAntiRecommender,
    anti_recommendations: tuple[AntiRecommendation, ...],
    model_response: str,
) -> None:
    """Test that OpenAiNormalAntiRecommender._parse_llm_response() yields parsed AntiRecommendations."""

    anti_recommendation_records = []

    anti_recommendation_records = list(
        open_ai_normal_anti_recommender._parse_llm_response(  # noqa: SLF001
            model_response
        )
    )
    assert tuple(anti_recommendation_records) == anti_recommendations


@pytest.mark.skipif(settings.ci, reason="don't have OpenAI key in CI")
def test_generate_anti_recommendations(  # noqa: PLR0913
    session_mocker: MockFixture,
    open_ai_normal_anti_recommender: NormalOpenAiAntiRecommender,
    record_key: str,
    record_type: RecordType,
    model_response: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that OpenAiNormalAntiRecommender.generate_anti_recommendations() yields AntiRecommendations of a given record key."""

    session_mocker.patch.object(
        NormalOpenAiAntiRecommender,
        "_generate_llm_response",
        return_value=model_response,
    )
    assert (
        anti_recommendations[0].title
        == next(
            iter(
                open_ai_normal_anti_recommender.generate_anti_recommendations(
                    record_key, record_type
                )
            )
        ).title
    )
