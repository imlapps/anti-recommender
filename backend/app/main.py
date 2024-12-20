from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import SecretStr

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.auth.supabase import SupabaseAuthService
from app.models import AuthToken, CredentialsError, Settings
from app.routers import router
from app.user import SupabaseUserService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """A lifespan event to persist variables in an app's state on startup."""

    settings = Settings()
    supabase_auth_service = SupabaseAuthService(settings=settings)
    supabase_user_service = SupabaseUserService(
        auth_service=supabase_auth_service, settings=settings
    )

    app.state.anti_recommendation_engine = AntiRecommendationEngine(
        user=supabase_user_service.create_user_from_token(
            authentication_token=AuthToken(access_token=SecretStr(""))
        ),
        settings=settings,
    )
    app.state.settings = settings
    app.state.user_service = supabase_user_service
    app.state.auth_service = supabase_auth_service

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.exception_handler(CredentialsError)
async def credentials_exception_handler(
    request: Request,  # noqa: ARG001
    exc: CredentialsError,  # noqa: ARG001
) -> RedirectResponse:
    """Redirect to /sign_in_anonymously when a CredentialsError is encountered."""

    return RedirectResponse("/sign_in_anonymously")
