import pytest
from pytest_mock import MockFixture

from app.anti_recommenders.open_ai import NormalOpenAiAntiRecommender
from app.models import settings
from app.models.types import AntiRecommenderType

ANTI_RECOMMENDER_TYPES = frozenset([AntiRecommenderType.OPEN_AI])


@pytest.fixture(autouse=True, params=ANTI_RECOMMENDER_TYPES, scope="module")
def _anti_recommender(
    request: pytest.FixtureRequest,
    session_mocker: MockFixture,
    model_response: str,
) -> None:
    """Run this fixture before all tests in the module, and mock AntiRecommenders based on parameterized types."""

    if request.param is AntiRecommenderType.OPEN_AI and settings.openai_api_key:
        session_mocker.patch.object(
            NormalOpenAiAntiRecommender,
            "_generate_llm_response",
            return_value=model_response,
        )
