import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.dependencies import *


def mock_wikipedia_articles():
    """Mock Wikipedia article values."""

    return tuple([{"wikipedia_article": "Test Wikipedia article info."}])


@pytest.fixture(scope="module")
def client_for_next_endpoint():
    """
    This fixture overrides the get_next_wikipedia_articles() dependency
    for the /next endpoint, and yields a TestClient object.
    """

    # Override get_next_wikipedia_articles function
    app.dependency_overrides[get_next_wikipedia_articles] = mock_wikipedia_articles

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def client_for_previous_endpoint():
    """
    This fixture overrides the get_previous_wikipedia_article() dependency
    for the /previous endpoint, and yields a TestClient object.
    """

    # Override get_previous_wikipedia_article function
    app.dependency_overrides[get_previous_wikipedia_article] = mock_wikipedia_articles

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def client_for_current_endpoint():
    """
    This fixture overrides the get_current_wikipedia_article() dependency
    for the /current endpoint, and yields a TestClient object.
    """

    # Override get_current_wikipedia_article function
    app.dependency_overrides[get_current_wikipedia_article] = mock_wikipedia_articles

    with TestClient(app) as test_client:
        yield test_client
