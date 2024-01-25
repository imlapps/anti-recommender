from fastapi import FastAPI, Request  
from contextlib import asynccontextmanager 
from fastapi.testclient import TestClient

from app.routers.helpers.helpers import * 
from app.storage.storage import storage as wikipedia_storage
from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy

@asynccontextmanager 
async def lifespan(app: FastAPI):
    """
    A lifespan event to test the storage of wikipedia data in the app state.
    """

    app.state.wikipedia_storage =   {
        "info": "test-wikipedia-article"
        }

    yield 

    app.state.wikipedia_storage = None 

# intialize the FastAPI app and pass in the lifespan event.
app = FastAPI(lifespan = lifespan)

@app.get("/")
async def get_app_state(request: Request):
    """
    A path operation function of the root endpoint.
    It returns the contents of the app state via the access_app_state method.  
    """
    
    return access_app_state(request)


def test_access_app_state() -> None:
    """
    Test to check that data is correctly stored in the app state and can be accessed during runtime.
    """
    
    with TestClient(app) as client:
        app_state_dictionary = client.get("/")
        assert app_state_dictionary.status_code == 200

        # Check that the key "wikipedia_storage is correctly stored in the app state
        assert app_state_dictionary.json()[0]["wikipedia_storage"] == {"info": "test-wikipedia-article"}
    

def test_generate_anti_recommendations_of_wikipedia_articles(mocker):
    """
    Test to check that the generate_wikipedia_articles method returns 
    a tuple of records if the anti-recommendations of an article are found in storage.
    """

    # mock variables
    mock_request = mocker.Mock()

    # variables to mock return values
    mock_article_records = tuple([{"article-record-1" :  {"info": "wikipedia-article-1"}}])
    mock_anti_recommender_proxy = AntiRecommenderProxy()
    
    # Mock a function
    mocker.patch("app.routers.helpers.helpers.access_app_state",
                                        return_value = tuple([{"wikipedia_storage": wikipedia_storage}]))

    # Mock an object and its methods
    mocker.patch.object(AntiRecommenderProxy, "get_title")
    mocker.patch.object(AntiRecommenderProxy, "set_title")
    mocker.patch.object(AntiRecommenderProxy, "generate_anti_recommendations",
                                               side_effect = (("test")))

    mocker.patch.object(wikipedia_storage, "set_current_title")
    mocker.patch.object(wikipedia_storage, "get_current_title")
    mocker.patch.object(wikipedia_storage, "add_title_to_stack")
    
    mocker.patch.object(wikipedia_storage, "get_article_records", return_value = mock_article_records)

    # Main test
    assert generate_wikipedia_articles(mock_anti_recommender_proxy, mock_request) == tuple([{"anti_recommendations": mock_article_records}])

def test_generate_no_anti_recommendations_of_wikipedia_articles(mocker):
    """
    Test to check that the generate_wikipedia_articles method returns  
    a dict with no records if the anti-recommendations of an article were not obtained.
    """

    # mock variables
    mock_request = mocker.Mock()

    # variables to mock return values
    mock_article_records = tuple([{}])
    mock_anti_recommender_proxy = AntiRecommenderProxy()

    # Mock a function
    mocker.patch("app.routers.helpers.helpers.access_app_state",
                                        return_value = tuple([{"wikipedia_storage": wikipedia_storage}]))

    # Mock an object and its methods
    mocker.patch.object(AntiRecommenderProxy, "get_title")
    mocker.patch.object(AntiRecommenderProxy, "set_title")
    mocker.patch.object(AntiRecommenderProxy, "generate_anti_recommendations",
                                               side_effect = (("test")))

    mocker.patch.object(wikipedia_storage, "set_current_title")
    mocker.patch.object(wikipedia_storage, "get_current_title")
    mocker.patch.object(wikipedia_storage, "add_title_to_stack")
    
    mocker.patch.object(wikipedia_storage, "get_article_records", return_value = None)

    # Main test
    assert generate_wikipedia_articles(mock_anti_recommender_proxy, mock_request) == tuple([{"anti_recommendations": mock_article_records}])
    


def test_retrieve_previous_wikipedia_article(mocker):
    """
    Test to check that the retrieve_previous_wikipedia_articles method 
    returns the previous articles in storage.
    """

    # mock variables
    mock_request = mocker.Mock()

    # Mock a function
    mocker.patch("app.routers.helpers.helpers.access_app_state",
                                         return_value = tuple([{"wikipedia_storage": wikipedia_storage}]))
     
    # Mock an object and its methods
    mocker.patch.object(wikipedia_storage, "pop_title_from_stack")
    mocker.patch.object(wikipedia_storage, "set_current_title")
    
    mocker.patch.object(wikipedia_storage, "get_current_record",  
                        return_value = tuple([{"previous-article-1" : 
                                       {"info": "previous-wikipedia-article-1"}}]))

    # Main test
    assert retrieve_previous_wikipedia_article(mock_request) == tuple([{"previous-article-1" : 
                                                                    {"info": "previous-wikipedia-article-1"}}])

