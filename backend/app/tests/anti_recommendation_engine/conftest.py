import pytest
from pytest_mock import MockFixture

from app.anti_recommenders.openai import NormalOpenaiAntiRecommender
from app.models import settings
from app.models.types import AntiRecommenderType, ModelResponse

ANTI_RECOMMENDER_TYPES = frozenset(
    [AntiRecommenderType.OPEN_AI, AntiRecommenderType.ARKG]
)


@pytest.fixture(autouse=True, params=ANTI_RECOMMENDER_TYPES, scope="module")
def _anti_recommender(
    request: pytest.FixtureRequest,
    session_mocker: MockFixture,
    model_response: ModelResponse,
    mock_database_fetch: None,
    mock_database_upsert: None,
) -> None:
    """Run this fixture before all tests in the module, and mock AntiRecommenders based on parameterized types."""

    if request.param is AntiRecommenderType.OPEN_AI and settings.openai_api_key:
        session_mocker.patch.object(
            NormalOpenaiAntiRecommender,
            "_generate_llm_response",
            return_value=model_response,
        )
    else:
        pytest.skip(reason="don't have OpenAI API Key.")

    if (
        request.param is AntiRecommenderType.ARKG
        and not settings.arkg_file_path.exists()
    ):
        pytest.skip(reason="don't have Wikipedia ARKG test file.")
