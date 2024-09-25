from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.anti_recommendation_engine import AntiRecommendationEngine
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
