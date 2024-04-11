from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.routers import router
from app.anti_recommendation_engine import AntiRecommendationEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A lifespan event to persist the AntiRecommendationEngine on start up.
    """

    app.state.anti_recommendation_engine = AntiRecommendationEngine()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
