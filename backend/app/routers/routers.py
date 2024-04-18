from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.models.record import Record
from app.models.types.record_type import RecordType
from app.routers.dependencies import next_records_parameters

router = APIRouter(prefix="/api/v1/nerdswipe", tags=["/api/v1/nerdswipe"])


@router.get("/next_records")
async def next_records(
    next_params: Annotated[dict, Depends(next_records_parameters)], request: Request
) -> tuple[Record, ...]:
    """
    This is the path operation function of the /next endpoint.
    Returns a tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.get_next_records(
        record_key=next_params["record_key"], record_type=next_params["record_type"]
    )


@router.get("/previous_records")
async def previous_records(request: Request) -> tuple[Record | None, ...]:
    """
    The path operation function of the /previous endpoint.
    Returns a tuple of previous Records stored in the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.get_previous_records()


@router.get("/initial_records")
async def initial_records(
    record_type: RecordType, request: Request
) -> tuple[Record, ...]:
    """
    A path operation function of the /initial_records endpoint.
    Returns the intial tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.get_initial_records(
        record_type=record_type
    )
