from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import AuthInvalidCredentialsException, AuthResult
from app.auth.supabase import supabase_auth_service as auth_service
from app.dependencies import check_user_authentication
from app.models import Credentials, Record, Token
from app.models.types import RecordKey
from app.user import User

router = APIRouter(prefix="/api/v1", tags=["/api/v1"])


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        sign_in_result: AuthResult = auth_service.sign_in(
            Credentials(email=form_data.username, password=form_data.password)
        )
    except AuthInvalidCredentialsException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to login. Encountered exception with the message: {exception.message}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    if not sign_in_result.succeeded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to login. Check username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return sign_in_result.authentication_token


@router.get("/sign_in_anonymously")
async def sign_in_anonymously() -> Token:
    sign_in_anonymously_result: AuthResult = auth_service.sign_in_anonymously()

    if not sign_in_anonymously_result.succeeded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable TO sign_in_anonymously.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return sign_in_anonymously_result.authentication_token


@router.post("/sign_up")
async def sign_up(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        sign_up_result: AuthResult = auth_service.sign_up(
            Credentials(email=form_data.username, password=form_data.password)
        )
    except AuthInvalidCredentialsException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signup. Encountered APIError with exception: {exception.message}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    if not sign_up_result.succeeded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to signup. Check username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return sign_up_result.authentication_token


@router.get("/sign_out")
async def sign_out() -> None:
    sign_out_result: AuthResult = auth_service.sign_out()

    if not sign_out_result.succeeded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to signout.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/next_records/{record_key}")
async def next_records(
    record_key: RecordKey,
    user_state: Annotated[User, Depends(check_user_authentication)],  # noqa: ARG001
    request: Request,
) -> tuple[Record, ...]:
    """
    The path operation function of the /next_records endpoint.

    Returns a tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.next_records(  # type: ignore[no-any-return]
        record_key=record_key
    )


@router.get("/previous_records")
async def previous_records(
    user_state: Annotated[User, Depends(check_user_authentication)],  # noqa: ARG001
    request: Request,
) -> tuple[Record | None, ...]:
    """
    The path operation function of the /previous_records endpoint.

    Returns a tuple of previous Records stored in the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.previous_records()  # type: ignore[no-any-return]


@router.get("/initial_records")
async def initial_records(
    user_state: Annotated[User, Depends(check_user_authentication)],  # noqa: ARG001
    request: Request,
) -> tuple[Record, ...]:
    """
    The path operation function of the /initial_records endpoint.

    Returns the intial tuple of Records from the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.initial_records()  # type: ignore[no-any-return]
