from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.routers import router

from app.storage_manager.storage.storage import Storage
from app.storage_manager.storage_manager import StorageManager

from backend.app.old.wikipedia_output_path import wikipedia_output_path


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A lifespan event to read in the Wikipedia output data and persist it in storage.
    """
    storage_manager = StorageManager(
        storage=Storage(), wikipedia_output_path=wikipedia_output_path
    )
    storage_manager.initialize_wikipedia_data()

    app.state.storage_manager = storage_manager

    yield

    app.state.storage_manager.reset_storage_manager()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
