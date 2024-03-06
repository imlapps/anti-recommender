from langchain.schema.runnable import RunnableSequence

from app.anti_recommender.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)


def test_create_query(open_ai_normal_anti_recommender, record_key):
    """Test that OpenAiNormalAntiRecommender._create_query() returns an OpenAI query when passed a record key."""

    assert record_key in open_ai_normal_anti_recommender._create_query(
        record_key=record_key
    )


def test_build_chain(open_ai_normal_anti_recommender):
    """Test that OpenAiNormalAntiRecommender._build_chain() initializes the OpenAiNormalAntiRecommender._open_ai_normal_chain."""

    open_ai_normal_anti_recommender._build_chain()

    assert isinstance(
        open_ai_normal_anti_recommender._open_ai_normal_chain, RunnableSequence
    )


def test_generate_response(
    mocker, open_ai_normal_anti_recommender, model_response, record_key
):
    """Test that OpenAiNormalAntiRecommender._generate_response() returns a response from an OpenAI large language model."""

    # Mock RunnableSerializable's invoke method and return an LLM response
    mocker.patch.object(
        RunnableSequence,
        "invoke",
        return_value=model_response,
    )

    open_ai_normal_anti_recommender._build_chain()

    assert (
        open_ai_normal_anti_recommender._generate_response(
            open_ai_normal_anti_recommender._create_query(record_key)
        )
        == model_response
    )


def test_parse_response(
    open_ai_normal_anti_recommender, anti_recommendations_tuple, model_response
):
    """Test that OpenAiNormalAntiRecommender._parse_response() yields parsed anti-recommendation records."""

    anti_recommendations = []
    for anti_recommendation in open_ai_normal_anti_recommender._parse_response(
        model_response
    ):
        anti_recommendations.append(anti_recommendation)

    assert (anti_recommendations) == anti_recommendations_tuple


def test_generate_anti_recommendations(mocker, open_ai_normal_anti_recommender, record_key, model_response, anti_recommendations_tuple):
    """Test that OpenAiNormalAntiRecommender.generate_anti_recommendations() yields anti-recommendations of a given record key."""

    mocker.patch.object(
        OpenAiNormalAntiRecommender,
        "_generate_response",
        return_value=model_response,
    )
    assert (anti_recommendations_tuple[0].title == next(
        open_ai_normal_anti_recommender.generate_anti_recommendations(record_key)).title)
