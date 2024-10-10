from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from gotrue.types import (
    AuthResponse,
    SignInWithEmailAndPasswordCredentials,
    SignUpWithEmailAndPasswordCredentials,
)
from postgrest import APIError

from app.auth import auth_client as auth_client
from app.dependencies import check_user_authentication
from app.models import Record, Token, UserState
from app.models.types import RecordKey

router = APIRouter(prefix="/api/v1", tags=["/api/v1"])


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        auth_response: AuthResponse | None = auth_client.sign_in(
            SignInWithEmailAndPasswordCredentials(
                email=form_data.username, password=form_data.password
            )
        )
    except APIError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to login. Encountered APIError with exception: {exception}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    if not auth_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to login. Check username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(**auth_response.session.model_dump())


@router.post("/sign_up")
async def sign_up(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        auth_response: AuthResponse | None = auth_client.sign_up(
            SignUpWithEmailAndPasswordCredentials(
                email=form_data.username, password=form_data.password
            )
        )
    except APIError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signup. Encountered APIError with exception: {exception}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    if not auth_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to signup. Check username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(**auth_response.session.model_dump())


@router.get("/sign_out")
async def sign_out() -> None:
    try:
        auth_client.sign_out()
    except APIError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to signout. Encountered APIError with exception: {exception}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception


@router.get("/next_records/{record_key}")
async def next_records(
    record_key: RecordKey,
    user_state: Annotated[  # noqa: ARG001
        UserState, Depends(check_user_authentication)
    ],
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
    user_state: Annotated[  # noqa: ARG001
        UserState, Depends(check_user_authentication)
    ],
    request: Request,
) -> tuple[Record | None, ...]:
    """
    The path operation function of the /previous_records endpoint.

    Returns a tuple of previous Records stored in the AntiRecommendationEngine.
    """

    return request.app.state.anti_recommendation_engine.previous_records()  # type: ignore[no-any-return]


@router.get("/initial_records")
async def initial_records(
    user_state: Annotated[UserState, Depends(check_user_authentication)],
    request: Request,
) -> tuple[Record, ...]:
    """
    The path operation function of the /initial_records endpoint.

    Returns the intial tuple of Records from the AntiRecommendationEngine.
    """
    request.app.state.anti_recommendation_engine.initialize_anti_recommender(
        user_state=user_state
    )

    if not user_state.anti_recommendations_history:
        last_seen_record_key = None
    else:
        last_seen_record_key = list(user_state.anti_recommendations_history).pop()
    return request.app.state.anti_recommendation_engine.initial_records(
        record_key=last_seen_record_key
    )  # type: ignore[no-any-return]
