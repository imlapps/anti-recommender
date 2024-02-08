from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A lifespan event to test the storage of wikipedia data in the app state.
    """

    app.state.wikipedia_storage = tuple([{"test-wikipedia-article": "test-info"}])

    yield

    app.state.wikipedia_storage = None


# intialize the FastAPI app and pass in the lifespan event.
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_wikipedia_storage():
    """
    A path operation function of the root endpoint.
    It returns wikipedia_storage, which was stored in the app state.
    """

    return app.state.wikipedia_storage


# Test that the root endpoint returns a value stored in the app's state.
def test_read_main():
    """
    Test to check that wikipedia_storage is correctly stored in the app state and can be accessed on startup.
    """

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()[0] == {"test-wikipedia-article": "test-info"}
