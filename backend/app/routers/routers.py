from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from app.routers.dependencies import *


router = APIRouter(prefix="/ap1/v1/wikipedia", tags=["/api/v1/wikipedia"])


@router.get("/next")
async def next(next_articles: Annotated[str, Depends(get_next_wikipedia_articles)]):
    """
    This is the path operation function of the /next endpoint.
    Returns a tuple of a Wikipedia article's anti-recommendations.
    """

    return next_articles


@router.get("/previous")
async def previous(
    previous_article: Annotated[str, Depends(get_previous_wikipedia_article)]
):
    """
    This is the path operation function of the /previous endpoint.
    Returns the previous Wikipedia article in storage.
    """

    return previous_article


@router.get("/current")
async def current(
    current_article: Annotated[str, Depends(get_current_wikipedia_article)]
):
    """
    A path operation function of the root endpoint.
    It returns the first Wikipedia record stored in wikipedia_storage.
    """

    return current_article
