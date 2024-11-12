import datetime
import os
import uuid
from collections.abc import AsyncIterator, Collection
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import gotrue.types as gotrue
import jwt
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from postgrest import APIResponse, SyncQueryRequestBuilder, SyncSelectRequestBuilder
from pydantic import AnyUrl
from pytest_mock import MockFixture
from supabase import SupabaseAuthClient

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.anti_recommenders.arkg import ArkgAntiRecommender
from app.anti_recommenders.openai import NormalOpenaiAntiRecommender
from app.auth.supabase import SupabaseAuthService
from app.models import AntiRecommendation, AuthToken, Record, Settings, wikipedia
from app.models.types import RdfMimeType, RecordKey
from app.models.types import StrippedString as ModelResponse
from app.readers import AllSourceReader
from app.readers.reader import WikipediaReader
from app.routers import router
from app.user import SupabaseUserService, User


@pytest.fixture(scope="session")
def openai_api_key() -> None:
    if "OPENAI_API_KEY" not in os.environ:
        pytest.skip(reason="don't have OpenAI API Key.")


@pytest.fixture(scope="session")
def supabase_parameters(settings: Settings) -> None:
    if not settings.supabase_url and not settings.supabase_key:
        pytest.skip(reason="don't have Supabase URL and Supabase key.")


@pytest.fixture(scope="session")
def test_data_directory_path() -> Path:
    """Return the Path of test data files."""

    return Path(__file__).parent.parent.absolute() / "data" / "test"


@pytest.fixture(scope="session")
def wikipedia_output_file_path(test_data_directory_path: Path) -> Path:
    """Return the Path of the Wikipedia output file."""

    wikipedia_output_file_path = test_data_directory_path / "mini-wikipedia.output.txt"
    if wikipedia_output_file_path.exists():
        return wikipedia_output_file_path

    pytest.skip(reason="don't have Wikipedia output test file.")


@pytest.fixture(scope="session")
def arkg_file_path(test_data_directory_path: Path) -> Path:
    """Return the file path of a Wikipedia ARKG."""

    wikipedia_arkg_file_path = test_data_directory_path / "wikipedia_arkg.ttl"

    if wikipedia_arkg_file_path.exists():
        return wikipedia_arkg_file_path

    pytest.skip(reason="don't have Wikipedia ARKG test file.")


@pytest.fixture(scope="session")
def settings(wikipedia_output_file_path: Path, arkg_file_path: Path) -> Settings:
    "Return a Settings object."

    _settings = Settings()
    _settings.arkg_file_path = arkg_file_path
    _settings.output_file_paths = frozenset([wikipedia_output_file_path])
    return _settings


@pytest.fixture(scope="session")
def all_source_reader(settings: Settings) -> AllSourceReader:
    """Return an AllSourceReader."""

    return AllSourceReader(settings=settings)


@pytest.fixture(scope="session")
def wikipedia_reader(wikipedia_output_file_path: Path) -> WikipediaReader:
    """Return a WikipediaReader."""

    return WikipediaReader(file_path=wikipedia_output_file_path)


@pytest.fixture(scope="session")
def openai_normal_anti_recommender(
    openai_api_key: None,  # noqa: ARG001
) -> NormalOpenaiAntiRecommender:
    """Return an OpenaiNormalAntiRecommender."""

    return NormalOpenaiAntiRecommender()


@pytest.fixture(scope="session")
def record_key() -> RecordKey:
    """Return a sample record key."""

    return "Nikola_Tesla"


@pytest.fixture(scope="session")
def model_response() -> ModelResponse:
    """Return a sample response from a large language model."""

    return "1 - Laplace's_demon - https://en.wikipedia.org/wiki/Laplace's_demon\n\
            2 - Leonardo_da_Vinci - https://en.wikipedia.org/wiki/Leonardo_da_Vinci"


@pytest.fixture(scope="session")
def anti_recommendations() -> tuple[AntiRecommendation, ...]:
    """Return a tuple of anti-recommendations."""

    return (
        AntiRecommendation(
            key="Laplace's_demon",
            url=AnyUrl("https://en.wikipedia.org/wiki/Laplace's_demon"),
        ),
        AntiRecommendation(
            key="Leonardo_da_Vinci",
            url=AnyUrl("https://en.wikipedia.org/wiki/Leonardo_da_Vinci"),
        ),
    )


@pytest.fixture(scope="session")
def serialized_records() -> tuple[dict[str, Collection[Collection[str]]], ...]:
    """Return a tuple of serialized records."""

    return (
        {
            "abstract_info": {
                "title": "Nikola_Tesla",
                "abstract": "A Serbian-American inventor, best known for his contributions to the design of \
                             the modern alternating current (AC) electricity supply system.",
                "url": "https://en.wikipedia.org/wiki/Nikola_Tesla",
            },
            "categories": (
                {
                    "text": "Nikola Tesla",
                    "link": "https://en.wikipedia.org/wiki/Category:Nikola_Tesla",
                },
                {
                    "text": "1856 Births",
                    "link": "https://en.wikipedia.org/wiki/Category:1856_births",
                },
                {
                    "text": "19th-century American engineers",
                    "link": "https://en.wikipedia.org/wiki/Category:19th-century_American_engineers",
                },
            ),
            "externallinks": (
                {
                    "title": "Austrian Empire",
                    "link": "https://en.wikipedia.org/wiki/Austrian_Empire",
                },
                {
                    "title": "Electric Power Industry",
                    "link": "https://en.wikipedia.org/wiki/Electric_power_industry",
                },
                {
                    "title": "Telephony",
                    "link": "https://en.wikipedia.org/wiki/Telephony",
                },
            ),
        },
        {
            "abstract_info": {
                "title": "Laplace's_demon",
                "abstract": "In the history of science, Laplace's demon was a notable published articulation \
                         of causal determinism on a scientific basis by Pierre-Simon Laplace in 1814.",
                "url": "https://en.wikipedia.org/wiki/Laplace's_demon",
            },
            "categories": (
                {
                    "text": "Pierre-Simon Laplace",
                    "link": "https://en.wikipedia.org/wiki/Category:Pierre-Simon_Laplace",
                },
                {
                    "text": "Determinism",
                    "link": "https://en.wikipedia.org/wiki/Category:Determinism",
                },
                {
                    "text": "Thought experiments",
                    "link": "https://en.wikipedia.org/wiki/Category:Thought_experiments",
                },
            ),
            "externallinks": (
                {
                    "title": "Classical mechanics",
                    "link": "https://en.wikipedia.org/wiki/Classical_mechanics",
                },
                {
                    "title": "History of Science",
                    "link": "https://en.wikipedia.org/wiki/History_of_science",
                },
                {
                    "title": "Momentum",
                    "link": "https://en.wikipedia.org/wiki/Momentum",
                },
            ),
        },
        {
            "abstract_info": {
                "title": "Leonardo_da_Vinci",
                "abstract": "An Italian polymath of the High Renaissance who was active as a painter, \
                                draughtsman, engineer, scientist, theorist, sculptor, and architect.",
                "url": "https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
            },
            "categories": (
                {
                    "text": "Leonardo da Vinci",
                    "link": "https://en.wikipedia.org/wiki/Category:Leonardo_da_Vinci",
                },
                {
                    "text": "1452 births",
                    "link": "https://en.wikipedia.org/wiki/Category:1452_births",
                },
                {
                    "text": "15th-century Italian mathematicians",
                    "link": "https://en.wikipedia.org/wiki/Category:15th-century_Italian_mathematicians",
                },
            ),
            "externallinks": (
                {"title": "Polymath", "link": "https://en.wikipedia.org/wiki/Polymath"},
                {
                    "title": "High Renaissance",
                    "link": "https://en.wikipedia.org/wiki/High_Renaissance",
                },
                {
                    "title": "Paleontology",
                    "link": "https://en.wikipedia.org/wiki/Paleontology",
                },
            ),
        },
    )


@pytest.fixture(scope="session")
def records(serialized_records: tuple[Any, ...]) -> tuple[Record, ...]:
    """Return a tuple of Records."""

    return tuple(
        wikipedia.Article(**record["abstract_info"], **record)
        for record in serialized_records
    )


@pytest.fixture(scope="session")
def records_by_key(records: tuple[Record, ...]) -> dict[RecordKey, Record]:
    """Return a dictionary of Records."""
    _records_by_key = {}

    for record in records:
        _records_by_key[record.key] = record

    return _records_by_key


@pytest.fixture(scope="session")
def mime_type() -> RdfMimeType:
    """Return the MIME Type of a Wikipedia ARKG file."""

    return RdfMimeType.TURTLE


@pytest.fixture(scope="session")
def supabase_auth_service(
    settings: Settings,
    supabase_parameters: None,  # noqa: ARG001
) -> SupabaseAuthService:
    """Return a SupabaseAuthService object."""

    return SupabaseAuthService(settings=settings)


@pytest.fixture(scope="session")
def supabase_user_service(
    settings: Settings,
    supabase_auth_service: SupabaseAuthService,
) -> SupabaseUserService:
    """Return a SupabaseUserService object."""

    return SupabaseUserService(auth_service=supabase_auth_service, settings=settings)


@pytest.fixture(scope="session")
def user(supabase_user_service: SupabaseUserService) -> User:
    """Return a User object."""

    return supabase_user_service.create_user_from_id(user_id=uuid.uuid4())


@pytest.fixture(scope="session")
def anti_recommendation_engine(
    settings: Settings,
    session_mocker: MockFixture,
    records: tuple[Record, ...],
    user: User,
) -> AntiRecommendationEngine:
    """Return an AntiRecommendationEngine."""

    session_mocker.patch.object(AllSourceReader, "read", return_value=records)

    return AntiRecommendationEngine(user=user, settings=settings)


@pytest.fixture(scope="session")
def mock_database_fetch(
    session_mocker: MockFixture, user: User, record_key: RecordKey
) -> None:
    """Mock a Supabase database client's select request builder."""

    session_mocker.patch.object(
        SyncSelectRequestBuilder,
        "execute",
        return_value=APIResponse(
            data=[{"user_id": user.id, "anti_recommendations_history": [record_key]}]
        ),
    )


@pytest.fixture(scope="session")
def mock_database_upsert(session_mocker: MockFixture) -> None:
    """Mock a Supabase database client's upsert request builder."""

    session_mocker.patch.object(
        SyncQueryRequestBuilder,
        "execute",
        return_value=APIResponse(data=[{"name": "N/A"}]),
    )


@pytest.fixture(scope="session")
def arkg_anti_recommender(
    arkg_file_path: Path,
    mime_type: RdfMimeType,
    mock_database_fetch: None,  # noqa: ARG001
    records_by_key: dict[RecordKey, Record],
    user: User,
) -> ArkgAntiRecommender:
    """Return an ArkgAntiRecommender."""

    return ArkgAntiRecommender(
        file_path=arkg_file_path,
        mime_type=mime_type,
        record_keys=tuple(records_by_key.keys()),
        user=user,
    )


@pytest.fixture(scope="session")
def form_data() -> OAuth2PasswordRequestForm:
    """Return an OAuth2 password flow form data."""

    return OAuth2PasswordRequestForm(username="Imlapps", password="Imlapps@2024!")


@pytest.fixture(scope="session")
def gotrue_user(user: User) -> gotrue.User:
    """Return a GoTrue User."""

    return gotrue.User(
        id=str(user.id),
        app_metadata={"app_metadata": ""},
        user_metadata={"user_metadata": ""},
        aud="",
        created_at=datetime.datetime.now(tz=datetime.UTC),
    )


@pytest.fixture(scope="session")
def session(gotrue_user: gotrue.User) -> gotrue.Session:
    """Return a GoTrue Session."""

    return gotrue.Session(
        access_token=jwt.encode({"some": "payload"}, "secret", algorithm="HS256"),
        refresh_token="",
        user=gotrue_user,
        token_type="Bearer",
        expires_in=1000,
    )


@pytest.fixture(scope="session")
def auth_response(
    gotrue_user: gotrue.User, session: gotrue.Session
) -> gotrue.AuthResponse:
    """Return a GoTrue AuthResponse."""

    return gotrue.AuthResponse(
        user=gotrue_user,
        session=session,
    )


@pytest.fixture(scope="session")
def authentication_token(session: gotrue.Session) -> AuthToken:
    """Return an authentication token."""

    return AuthToken(**session.model_dump())


@pytest.fixture(scope="session")
def mock_get_user(session_mocker: MockFixture, gotrue_user: gotrue.User) -> None:
    """Mock a SupabaseAuthClient's get_user method."""

    session_mocker.patch.object(
        SupabaseAuthClient,
        "get_user",
        return_value=gotrue.UserResponse(user=gotrue_user),
    )


@pytest.fixture(scope="session")
def auth_header(authentication_token: AuthToken) -> dict[str, str]:
    """Return an Authorization header for HTTP requests."""

    if not authentication_token.access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No access token"
        )

    return {"Authorization": f"Bearer {authentication_token.access_token}"}


@pytest_asyncio.fixture(loop_scope="session")
async def app(
    anti_recommendation_engine: AntiRecommendationEngine,
    settings: Settings,
    supabase_user_service: SupabaseUserService,
    supabase_auth_service: SupabaseAuthService,
) -> AsyncIterator:
    "Yield a FastAPI app from a LifespanManager."

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.anti_recommendation_engine = anti_recommendation_engine
        app.state.auth_service = supabase_auth_service
        app.state.settings = settings
        app.state.user_service = supabase_user_service
        yield

    app = FastAPI(
        lifespan=lifespan,
    )

    app.include_router(router)
    async with LifespanManager(app) as manager:
        yield manager.app
