from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.auth import AuthException, AuthResponse

from app.dependencies import check_user_authentication
from app.models import AuthToken, Credentials, Record
from app.models.types import RecordKey


router = APIRouter(prefix="/api/v1", tags=["/api/v1"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
) -> AuthToken:

    try:
        sign_in_result: AuthResponse = request.app.state.auth_service.sign_in(
            Credentials(
                email=form_data.username, password=SecretStr(form_data.password)
            )
        )
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to login. Encountered AuthException with message: {exception.message}",
        ) from exception

    request.app.state.anti_recommendation_engine = AntiRecommendationEngine(  # type: ignore[no-any-return]
        user=request.app.state.user_service.create_user_from_token(
            sign_in_result.authentication_token
        ),
        settings=request.app.state.settings,
    )

    return sign_in_result.authentication_token


@router.get("/sign_in_anonymously")
async def sign_in_anonymously(request: Request) -> AuthToken:

    try:
        sign_in_anonymously_result: AuthResponse = (
            request.app.state.auth_service.sign_in_anonymously()
        )
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable To sign_in_anonymously. Encountered AuthException with message: {exception.message}",
        ) from exception

    return sign_in_anonymously_result.authentication_token


@router.post("/sign_up")
async def sign_up(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
) -> AuthToken:

    try:
        sign_up_result: AuthResponse = request.app.state.auth_service.sign_up(
            Credentials(
                email=form_data.username, password=SecretStr(form_data.password)
            )
        )
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signup. Encountered AuthException with message: {exception.message}",
        ) from exception

    request.app.state.anti_recommendation_engine = AntiRecommendationEngine(  # type: ignore[no-any-return]
        user=request.app.state.user_service.create_user_from_token(
            sign_up_result.authentication_token
        ),
        settings=request.app.state.settings,
    )

    return sign_up_result.authentication_token


@router.get("/sign_out")
async def sign_out(request: Request) -> None:
    try:
        request.app.state.auth_service.sign_out()
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signout. Encountered AuthException with message: {exception.message}",
        ) from exception


@router.get(
    "/next_records/{record_key}", dependencies=[Depends(check_user_authentication)]
)
async def next_records(
    record_key: RecordKey,
    request: Request,
) -> tuple[Record, ...]:
    """
    The path operation function of the /next_records endpoint.

    Returns a tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.next_records(  # type: ignore[no-any-return]
        record_key=record_key
    )


@router.get("/previous_records", dependencies=[Depends(check_user_authentication)])
async def previous_records(request: Request) -> tuple[Record | None, ...]:
    """
    The path operation function of the /previous_records endpoint.

    Returns a tuple of previous Records stored in the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.previous_records()  # type: ignore[no-any-return]


@router.get("/initial_records", dependencies=[Depends(check_user_authentication)])
async def initial_records(request: Request) -> tuple[Record, ...]:
    """
    The path operation function of the /initial_records endpoint.

    Returns the intial tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.initial_records()  # type: ignore[no-any-return]
