from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from pytest_mock import MockFixture
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)


def test_generate_anti_recommendations(
    mocker: MockFixture,
    anti_recommender_proxy: AntiRecommenderProxy,
    record_key: str,
    anti_recommendations: tuple[AntiRecommendation, ...],
    model_response: str,
) -> None:
    """Test that AntiRecommenderProxy.generate_anti_recommendations() yields anti-recommendations of a given record key."""

    # Mock the large language model call in the OpenAiNormalAntiRecommender.generate_response() and return a sample model response.
    mocker.patch.object(
        OpenAiNormalAntiRecommender, "generate_response", return_value=model_response
    )

    anti_recommendation_records = []

    anti_recommendation_records = list(
        anti_recommender_proxy.generate_anti_recommendations(record_key)
    )
    assert tuple(anti_recommendation_records) == anti_recommendations
