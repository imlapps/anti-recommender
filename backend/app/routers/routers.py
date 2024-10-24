from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.auth import AuthException, AuthResponse
from app.auth.supabase import SupabaseAuthService
from app.dependencies import check_user_authentication
from app.models import AuthToken, Credentials, Record, settings
from app.models.types import RecordKey
from app.user import SupabaseUserService

router = APIRouter(prefix="/api/v1", tags=["/api/v1"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
) -> AuthToken:
    supabase_auth_service = SupabaseAuthService(settings=settings)

    try:
        sign_in_result: AuthResponse = supabase_auth_service.sign_in(
            Credentials(
                email=form_data.username, password=SecretStr(form_data.password)
            )
        )
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to login. Encountered AuthException with message: {exception.message}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    supabase_user_service = SupabaseUserService(
        auth_service=supabase_auth_service, settings=settings
    )

    request.app.state.anti_recommendation_engine = AntiRecommendationEngine(  # type: ignore[no-any-return]
        user=supabase_user_service.create_user_from_token(
            sign_in_result.authentication_token
        ),
        settings=settings,
    )

    return sign_in_result.authentication_token


@router.get("/sign_in_anonymously")
async def sign_in_anonymously() -> AuthToken:
    supabase_auth_service = SupabaseAuthService(settings=settings)

    try:
        sign_in_anonymously_result: AuthResponse = (
            supabase_auth_service.sign_in_anonymously()
        )
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable To sign_in_anonymously. Encountered AuthException with message: {exception.message}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    return sign_in_anonymously_result.authentication_token


@router.post("/sign_up")
async def sign_up(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
) -> AuthToken:
    supabase_auth_service = SupabaseAuthService(settings=settings)

    try:
        sign_up_result: AuthResponse = supabase_auth_service.sign_up(
            Credentials(
                email=form_data.username, password=SecretStr(form_data.password)
            )
        )
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signup. Encountered AuthException with message: {exception.message}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    supabase_user_service = SupabaseUserService(
        auth_service=supabase_auth_service, settings=settings
    )

    request.app.state.anti_recommendation_engine = AntiRecommendationEngine(  # type: ignore[no-any-return]
        user=supabase_user_service.create_user_from_token(
            sign_up_result.authentication_token
        ),
        settings=settings,
    )

    return sign_up_result.authentication_token


@router.get("/sign_out")
async def sign_out() -> None:
    supabase_auth_service = SupabaseAuthService(settings=settings)

    try:
        supabase_auth_service.sign_out()
    except AuthException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signout. Encountered AuthException with message: {exception.message}",
            headers={"WWW-Authenticate": "Bearer"},
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
