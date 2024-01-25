from typing import Tuple, Dict
from fastapi import Request 

from fastapi import Depends, Request
from typing_extensions import Annotated 

from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy 


__all__ = ['access_app_state', 'generate_wikipedia_articles', 'retrieve_previous_wikipedia_article']


def access_app_state(request:Request) -> Tuple[Dict, ...]:
    """
    This method returns variables of the app's state as a dictionary in a tuple
    """ 

    return tuple([{"wikipedia_storage": request.app.state.wikipedia_storage}])


def generate_wikipedia_articles(anti_recommender: Annotated[AntiRecommenderProxy, Depends()], request:Request) -> Tuple[Dict, ...]:
    """
    This method returns a tuple that contains an article's anti-recommendation records.
    An an empty tuple (with an empty dict) is returned if no anti-recommendations are obtained.
    """
    
    wikipedia_storage = access_app_state(request)[0]["wikipedia_storage"]

    # If no title is given, use the current title in storage as the anti-recommender's title
    if anti_recommender.get_title() == None:
        anti_recommender.set_title(wikipedia_storage.get_current_title())

    wikipedia_articles = []
    
    # This loop retrieves the records of the anti-recommendations if they exist in storage
    # Each article is a tuple of the form: (wikipedia_title, wikipedia_url)
    for article in anti_recommender.generate_anti_recommendations():
        article_record = wikipedia_storage.get_article_records(article[0])

        if article_record != None:
            wikipedia_articles.append(article_record[0])
    
    # Add the current title to the stack. This is now the previous article in storage.
    wikipedia_storage.add_title_to_stack(wikipedia_storage.get_current_title())
    
    # Set the first item in wikipedia_articles as the new current title in storage.
    if len(wikipedia_articles) == 0:
        wikipedia_articles.append({})
        wikipedia_storage.set_current_title("")
    else:   
        wikipedia_storage.set_current_title(list(wikipedia_articles[0].keys())[0])


    return tuple([{"anti_recommendations": tuple(wikipedia_articles)}])
    


def retrieve_previous_wikipedia_article(request: Request) -> Tuple[Dict, ...]:

    """
    This method retrieves the previous Wikipedia article from storage.
    """

    wikipedia_storage = access_app_state(request)[0]["wikipedia_storage"]
    wikipedia_storage.set_current_title(wikipedia_storage.pop_title_from_stack())

    return wikipedia_storage.get_current_record()