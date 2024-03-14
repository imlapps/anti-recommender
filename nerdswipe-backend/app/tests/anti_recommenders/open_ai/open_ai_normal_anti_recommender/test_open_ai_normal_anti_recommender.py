from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from pytest_mock import MockFixture

from langchain.schema.runnable import RunnableSequence

from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)


def test_create_query(
    open_ai_normal_anti_recommender: OpenAiNormalAntiRecommender, record_key: str
) -> None:
    """Test that OpenAiNormalAntiRecommender._create_query() returns an OpenAI query when passed a record key."""

    assert record_key in open_ai_normal_anti_recommender._create_query(  # noqa: SLF001
        record_key
    )


def test_build_chain(
    open_ai_normal_anti_recommender: OpenAiNormalAntiRecommender,
) -> None:
    """Test that OpenAiNormalAntiRecommender._build_chain() initializes the OpenAiNormalAntiRecommender._open_ai_normal_chain."""

    open_ai_normal_anti_recommender._build_chain()  # noqa: SLF001

    assert isinstance(
        open_ai_normal_anti_recommender.open_ai_normal_chain, RunnableSequence
    )


def test_generate_response(
    mocker: MockFixture,
    open_ai_normal_anti_recommender: OpenAiNormalAntiRecommender,
    model_response: str,
    record_key: str,
) -> None:
    """Test that OpenAiNormalAntiRecommender._generate_response() returns a response from an OpenAI large language model."""

    # Mock RunnableSerializable's invoke method and return an LLM response
    mocker.patch.object(
        RunnableSequence,
        "invoke",
        return_value=model_response,
    )

    open_ai_normal_anti_recommender._build_chain()  # noqa: SLF001

    assert (
        open_ai_normal_anti_recommender._generate_response(  # noqa: SLF001
            open_ai_normal_anti_recommender._create_query(record_key)  # noqa: SLF001
        )
        == model_response
    )


def test_parse_response(
    open_ai_normal_anti_recommender: OpenAiNormalAntiRecommender,
    anti_recommendations: tuple[AntiRecommendation, ...],
    model_response: str,
) -> None:
    """Test that OpenAiNormalAntiRecommender._parse_response() yields parsed anti-recommendation records."""

    anti_recommendation_records = []

    anti_recommendation_records = list(
        open_ai_normal_anti_recommender._parse_response(model_response)  # noqa: SLF001
    )
    assert tuple(anti_recommendation_records) == anti_recommendations


def test_generate_anti_recommendations(
    mocker: MockFixture,
    open_ai_normal_anti_recommender: OpenAiNormalAntiRecommender,
    record_key: str,
    model_response: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that OpenAiNormalAntiRecommender.generate_anti_recommendations() yields anti-recommendations of a given record key."""

    mocker.patch.object(
        OpenAiNormalAntiRecommender,
        "_generate_response",
        return_value=model_response,
    )
    assert (
        anti_recommendations[0].title
        == next(
            open_ai_normal_anti_recommender.generate_anti_recommendations(record_key)
        ).title
    )
