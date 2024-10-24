from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import SecretStr

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.auth.supabase import SupabaseAuthService
from app.models import AuthToken, CredentialsError, settings
from app.routers import router
from app.user import SupabaseUserService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    A lifespan event to persist the AntiRecommendationEngine on start up.

    """

    supabase_user_service = SupabaseUserService(
        auth_service=SupabaseAuthService(settings=settings), settings=settings
    )

    app.state.anti_recommendation_engine = AntiRecommendationEngine(
        user=supabase_user_service.create_user_from_token(
            AuthToken(access_token=SecretStr(""))
        ),
        settings=settings,
    )

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.exception_handler(CredentialsError)
async def credentials_exception_handler(
    request: Request,  # noqa: ARG001
    exc: CredentialsError,  # noqa: ARG001
) -> RedirectResponse:
    return RedirectResponse("/sign_in_anonymously")
