from fastapi.testclient import TestClient
from typing import Tuple, Dict  

from app.main import app
from app.routers.helpers.helpers import * 


async def mock_generate_wikipedia_articles() -> Tuple[Dict, ...]:
    """This is a method to mock the generate_wikipedia_article function."""

    return tuple([{
        "anti_recommendations" : ({"article-1":{"info":"wikipedia-article-1"}})
           }])

async def mock_retrieve_previous_wikipedia_article() -> Tuple[Dict, ...]:
    """This is a method to mock the retrieve_previous_wikipedia_article function."""

    return tuple([{
        "previous-article" : 
                        {
                            "info" : "previous-wikipedia-article"
                        }
          }])

# initialize the test client
client = TestClient(app)

# Override generate_wikipedia_articles function 
app.dependency_overrides[generate_wikipedia_articles] = mock_generate_wikipedia_articles

# Override retrieve_previous_wikipedia_article function 
app.dependency_overrides[retrieve_previous_wikipedia_article] = mock_retrieve_previous_wikipedia_article


def test_next():
    """
    Tests an endpoint /next with a mock tuple of Wikipedia articles
    """

    response = client.get(url="/anti_recommendation/next")
    assert response.status_code == 200 
    assert response.json()[0].get("anti_recommendations") == {"article-1":{"info":"wikipedia-article-1"}}


def test_previous(): 
    """
    Tests the endpoint /previous with a mock dict of a Wikipedia article 
    """

    response = client.get(url="/anti_recommendation/previous")
    assert response.status_code == 200
    assert response.json()[0].get("previous-article") == {"info" : "previous-wikipedia-article"}