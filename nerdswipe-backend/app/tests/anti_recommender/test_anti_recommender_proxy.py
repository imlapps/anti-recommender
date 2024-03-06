from app.anti_recommender.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import OpenAiNormalAntiRecommender


def test_generate_anti_recommendations(mocker, anti_recommender_proxy, record_key, anti_recommendations_tuple, model_response):
    """Test that AntiRecommenderProxy.generate_anti_recommendations() yields anti-recommendations of a given record key."""

    # Mock the large language model call in the OpenAiNormalAntiRecommender._generate_response() and return a sample model response.
    mocker.patch.object(OpenAiNormalAntiRecommender, "_generate_response",
                        return_value=model_response)

    anti_recommendations = []

    for anti_recommendation in anti_recommender_proxy.generate_anti_recommendations(record_key):
        anti_recommendations.append(anti_recommendation)

    assert ((anti_recommendations) == anti_recommendations_tuple)
