from fastapi.testclient import TestClient

from app.main import app
from app.routers.dependencies import *


def mock_current_wikipedia_article():
    return tuple(
        [
            {
                "current_article": {
                    "test-info": "test info for test-current-article-1"
                },
            }
        ]
    )


def mock_next_wikipedia_articles():
    return tuple(
        [
            {
                "next_articles": {"test-info": "test info for test-next-article-1"},
            }
        ]
    )


def mock_previous_wikipedia_article():
    return tuple(
        [
            {
                "previous_article": {
                    "test-info": "test info for test-previous-article-1"
                },
            }
        ]
    )


# initialize the test client
client = TestClient(app)

# Override get_next_wikipedia_articles function
app.dependency_overrides[get_next_wikipedia_articles] = mock_next_wikipedia_articles

# Override get_previous_wikipedia_article function
app.dependency_overrides[get_previous_wikipedia_article] = (
    mock_previous_wikipedia_article
)

# Override get_current_wikipedia_article function
app.dependency_overrides[get_current_wikipedia_article] = mock_current_wikipedia_article


def test_next():
    """
    Tests an endpoint /next with a mock method that returns a tuple of a Wikipedia article.
    """

    response = client.get(url="/ap1/v1/wikipedia/next")
    assert response.status_code == 200
    assert response.json()[0].get("next_articles") == {
        "test-info": "test info for test-next-article-1"
    }


def test_previous():
    """
    Tests the endpoint /previous with a mock method that returns a tuple of a Wikipedia article.
    """

    response = client.get(url="/ap1/v1/wikipedia/previous")
    assert response.status_code == 200
    assert response.json()[0].get("previous_article") == {
        "test-info": "test info for test-previous-article-1"
    }


def test_current():
    """
    Tests the endpoint /current with a mock method that returns a tuple of a Wikipedia article.
    """

    response = client.get(url="/ap1/v1/wikipedia/current")
    assert response.status_code == 200
    assert response.json()[0].get("current_article") == {
        "test-info": "test info for test-current-article-1"
    }
