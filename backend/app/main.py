from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.models.credentials_error import CredentialsError
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    A lifespan event to persist the AntiRecommendationEngine on start up.
    """

    app.state.anti_recommendation_engine = AntiRecommendationEngine()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.exception_handler(CredentialsError)
async def credentials_exception_handler(
    request: Request,
    exc: CredentialsError,  # noqa: ARG001
) -> RedirectResponse:
    return RedirectResponse("/login")
