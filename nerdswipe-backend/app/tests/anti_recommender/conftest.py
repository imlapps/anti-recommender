import pytest
from typing import Generator, Tuple

from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from app.anti_recommender.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)
from app.anti_recommender.anti_recommender_proxy import AntiRecommenderProxy


@pytest.fixture
def anti_recommender_proxy() -> Generator[AntiRecommenderProxy, None, None]:
    """Yield an AntiRecommenderProxy object."""

    yield AntiRecommenderProxy()


@pytest.fixture
def open_ai_normal_anti_recommender() -> (
    Generator[OpenAiNormalAntiRecommender, None, None]
):
    """Yield an OpenAiNormalAntiRecommender object."""
    yield OpenAiNormalAntiRecommender()


@pytest.fixture
def record_key() -> str:
    """Return a sample record key."""

    return "Nikola Tesla"


@pytest.fixture
def model_response() -> str:
    """Return a sample response from a large language model."""

    return "1 - Laplace's Demon - https://en.wikipedia.org/wiki/Laplace's_demon\n\
            2 - Leonardo da Vinci - https://en.wikipedia.org/wiki/Leonardo_da_Vinci"


@pytest.fixture
def anti_recommendations_tuple() -> Tuple[AntiRecommendation, ...]:
    """Return a tuple of anti-recommendations."""

    return (
        [
            AntiRecommendation(
                title="Laplace's Demon",
                url="https://en.wikipedia.org/wiki/Laplace's_demon",
            ),
            AntiRecommendation(
                title="Leonardo da Vinci",
                url="https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
            ),
        ]
    )
