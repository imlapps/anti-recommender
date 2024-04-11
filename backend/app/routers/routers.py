from fastapi import Request, APIRouter, Depends
from typing_extensions import Annotated

from app.models.record import Record
from app.routers.dependencies import next_parameters

router = APIRouter(prefix="/ap1/v1/nerdswipe",
                   tags=["/api/v1/nerdswipe"])


@router.get("/next")
async def next(next_params: Annotated[dict, Depends(next_parameters)], request: Request) -> tuple[Record, ...]:
    """
    This is the path operation function of the /next endpoint.
    Returns a tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.get_next_records(
        next_params['record_key'], next_params['record_type'])


@router.get("/previous")
async def previous(request: Request
                   ) -> tuple[Record | None, ...]:
    """
    The path operation function of the /previous endpoint.
    Returns a tuple of previous Records stored in the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.get_previous_records()


@router.get("/current")
async def current(
    record_type: str, request: Request
) -> tuple[Record, ...]:
    """
    A path operation function of the root endpoint.
    Returns the intial tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.get_initial_records(
        record_type)
