from fastapi import Request

from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy

__all__ = [
    "get_next_wikipedia_articles",
    "get_previous_wikipedia_article",
    "get_current_wikipedia_article",
]


def get_next_wikipedia_articles(request: Request):
    """
    This method retrieves a tuple of a Wikipedia article's anti-recommendations from storage
    and returns it to the /next endpoint.
    """

    return request.app.state.storage_manager.retrieve_next_wikipedia_articles(
        AntiRecommenderProxy()
    )


def get_previous_wikipedia_article(request: Request):
    """
    This method retrieves a tuple of the previous Wikipedia article in storage
    returns it to the /previous endpoint.
    """

    return request.app.state.storage_manager.retrieve_previous_wikipedia_article()


def get_current_wikipedia_article(request: Request):
    """
    This method retrieves a tuple of the current Wikipedia article in storage
    returns it to the /current endpoint.
    """

    return request.app.state.storage_manager.retrieve_current_wikipedia_article()
