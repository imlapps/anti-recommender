import os
import pytest

from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy
from app.anti_recommenders.open_ai.regular_open_ai_anti_recommender import (
    RegularOpenAiAntiRecommender,
)

SAMPLE_TITLE = "Wikipedia Title"
SAMPLE_PARSED_MODEL_RESPONSE = tuple([("Title", "https://en.wikipedia.org/wiki/Title")])
SAMPLE_MODEL_RESPONSE = "1 - Title - https://en.wikipedia.org/wiki/Title"


@pytest.fixture(scope="class", params=["openai"])
def anti_recommender_type(request):
    """This fixture returns different model types as a parameter."""
    return request.param


@pytest.fixture(scope="class")
def anti_recommender_proxy(anti_recommender_type):
    """
    This fixture returns an AntiRecommenderProxy object.
    It uses the return values of the anti_recommender_type fixture.
    """
    return AntiRecommenderProxy(type=anti_recommender_type)


@pytest.fixture(scope="class")
def anti_recommender_object(anti_recommender_type):
    """
    This fixture returns an AntiRecommender type as a String.
    It uses the return values of the anti_recommender_type fixture.
    """

    if anti_recommender_type == "openai":
        if "OPENAI_API_KEY" in os.environ:
            return "RegularOpenAiAntiRecommender"


class Title:
    """
    This class contains a suite of tests that ensure that the setter and getter of the AntiRecommenderProxy's title work as expected.
    """

    def test_title(self, anti_recommender_proxy):
        """Test that the title that was set in the AntiRecommenderProxy matches the title that was returned."""
        anti_recommender_proxy.title = SAMPLE_TITLE
        assert anti_recommender_proxy.title == SAMPLE_TITLE


class GenerateAntiRecommendation:
    """
    This class contains a suite of tests that ensure that AntiRecommenderProxy.generate_anti_recommendations() works as expected.
    """

    def test_generate_anti_recommendations(
        mocker, anti_recommender_proxy, anti_recommender_object
    ):
        """Test that the AntiRecommenderProxy successfully generates anti-recommendations."""

        if anti_recommender_object == "RegularOpenAiAntiRecommender":

            # Mock RegularOpenAiAntiRecommender's _parse_response method and return a sample response
            mocker.patch.object(
                RegularOpenAiAntiRecommender,
                "_generate_response",
                return_value=SAMPLE_MODEL_RESPONSE,
            )

        assert (
            anti_recommender_proxy.generate_anti_recommendations()
            == SAMPLE_PARSED_MODEL_RESPONSE
        )
