from langchain.schema.runnable import RunnableSequence, RunnableSerializable
from pytest_mock import MockFixture

from app.anti_recommenders.openai import NormalOpenaiAntiRecommender
from app.models import AntiRecommendation
from app.models.types import RecordKey
from app.models.types import StrippedString as ModelResponse


def test_build_chain(
    openai_normal_anti_recommender: NormalOpenaiAntiRecommender,
) -> None:
    """Test that OpenaiNormalAntiRecommender._build_chain() returns an OpenAI chain of type RunnableSerializable."""

    assert isinstance(
        openai_normal_anti_recommender._build_chain(),  # noqa: SLF001
        RunnableSerializable,
    )


def test_create_query(
    openai_normal_anti_recommender: NormalOpenaiAntiRecommender,
    record_key: RecordKey,
) -> None:
    """Test that OpenaiNormalAntiRecommender._create_query() returns an OpenAI query when passed a record key."""

    assert record_key in openai_normal_anti_recommender._create_query(  # noqa: SLF001
        record_key=record_key
    )


def test_generate_llm_response(
    session_mocker: MockFixture,
    openai_normal_anti_recommender: NormalOpenaiAntiRecommender,
    model_response: ModelResponse,
    record_key: RecordKey,
) -> None:
    """Test that OpenaiNormalAntiRecommender._generate_llm_response() returns a response from an OpenAI large language model."""

    # Mock RunnableSerializable's invoke method and return an LLM response
    session_mocker.patch.object(
        RunnableSequence,
        "invoke",
        return_value=model_response,
    )

    assert (
        openai_normal_anti_recommender._generate_llm_response(  # noqa: SLF001
            open_ai_query=openai_normal_anti_recommender._create_query(  # noqa: SLF001
                record_key=record_key
            ),
            open_ai_chain=openai_normal_anti_recommender._build_chain(),  # noqa: SLF001
        )
        == model_response
    )


def test_parse_llm_response(
    openai_normal_anti_recommender: NormalOpenaiAntiRecommender,
    anti_recommendations: tuple[AntiRecommendation, ...],
    model_response: ModelResponse,
) -> None:
    """Test that OpenaiNormalAntiRecommender._parse_llm_response() yields parsed AntiRecommendations."""

    anti_recommendation_records = []

    anti_recommendation_records = list(
        openai_normal_anti_recommender._parse_llm_response(  # noqa: SLF001
            model_response
        )
    )
    assert tuple(anti_recommendation_records) == anti_recommendations


def test_generate_anti_recommendations(
    session_mocker: MockFixture,
    openai_normal_anti_recommender: NormalOpenaiAntiRecommender,
    record_key: RecordKey,
    model_response: ModelResponse,
    anti_recommendations: tuple[AntiRecommendation, ...],
) -> None:
    """Test that OpenaiNormalAntiRecommender.generate_anti_recommendations() yields AntiRecommendations of a given record key."""

    session_mocker.patch.object(
        NormalOpenaiAntiRecommender,
        "_generate_llm_response",
        return_value=model_response,
    )
    assert (
        anti_recommendations[0].key
        == next(
            iter(
                openai_normal_anti_recommender.generate_anti_recommendations(
                    record_key=record_key
                )
            )
        ).key
    )
