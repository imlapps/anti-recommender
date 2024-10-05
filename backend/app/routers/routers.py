from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.models import Record
from app.models.query_params import NextRecordsQueryParams

router = APIRouter(prefix="/api/v1", tags=["/api/v1"])


@router.get("/next_records")
async def next_records(
    next_params: Annotated[NextRecordsQueryParams, Depends(NextRecordsQueryParams)],
    request: Request,
) -> tuple[Record, ...]:
    """
    The path operation function of the /next_records endpoint.

    Returns a tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.next_records(  # type: ignore[no-any-return]
        record_key=next_params.record_key
    )


@router.get("/previous_records")
async def previous_records(request: Request) -> tuple[Record | None, ...]:
    """
    The path operation function of the /previous_records endpoint.

    Returns a tuple of previous Records stored in the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.previous_records()  # type: ignore[no-any-return]


@router.get("/initial_records")
async def initial_records(
    request: Request,
) -> tuple[Record, ...]:
    """
    The path operation function of the /initial_records endpoint.

    Returns the intial tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.initial_records()  # type: ignore[no-any-return]
