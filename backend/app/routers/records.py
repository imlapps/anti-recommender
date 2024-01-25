from fastapi import Depends, APIRouter

from typing_extensions import Annotated, Tuple, Dict 

from .helpers.helpers import *

router = APIRouter(
    prefix = "/records",
    tags = ["records"]
) 

@router.get("/next")
async def next(wikipedia_articles: Annotated[dict, Depends(generate_wikipedia_articles)]):
    """ 
        This is the path operation function of the /next endpoint. 
        Returns a tuple of a Wikipedia article's anti-recommendations.
    """
    
    return wikipedia_articles

@router.get("/previous")
async def previous(previous_article: Annotated[str, Depends(retrieve_previous_wikipedia_article)]):
    """ 
        This is the path operation function of the /previous endpoint.
        Returns the previous Wikipedia article in storage.
    """
    
    return previous_article
