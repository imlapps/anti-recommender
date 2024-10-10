from datetime import datetime
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
import pytest
import jwt
from app.main import app
from app.models import Token
from app.models.types import RecordKey
from pytest_mock import MockFixture

from app.models.user import User

OK_STATUS_CODE = 200

from fastapi import HTTPException
from supabase import SupabaseAuthClient
import gotrue.types as gotrue


def get_auth_header(access_token: str | None) -> dict[str, str]:
    if not access_token:
        raise HTTPException(status_code=401, detail="No access token")
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="session")
def form_data() -> OAuth2PasswordRequestForm:
    return OAuth2PasswordRequestForm(username="Imlapps", password="Imlapps@2024!")


@pytest.fixture(scope="session")
def gotrue_user(user: User) -> gotrue.User:
    return gotrue.User(
        id=str(user.id),
        app_metadata={"app_metadata": ""},
        user_metadata={"user_metadata": ""},
        aud="",
        created_at=datetime.now(),
    )


@pytest.fixture(scope="session")
def session(gotrue_user: gotrue.User) -> gotrue.Session:
    return gotrue.Session(
        access_token=jwt.encode({"some": "payload"}, "secret", algorithm="HS256"),
        refresh_token="random_refresh_token",
        user=gotrue_user,
        token_type="Bearer",
        expires_in=1000,
    )


@pytest.fixture(scope="session")
def auth_response(
    gotrue_user: gotrue.User, session: gotrue.Session
) -> gotrue.AuthResponse:
    return gotrue.AuthResponse(
        user=gotrue_user,
        session=session,
    )


@pytest.fixture(scope="session")
def token(session: gotrue.Session) -> Token:
    return Token(**session.model_dump())


def test_login(
    session_mocker: MockFixture,
    form_data: OAuth2PasswordRequestForm,
    auth_response: gotrue.AuthResponse,
) -> None:
    """
    Test the /login endpoint.
    """

    # headers = get_auth_header(access_token=token.access_token)

    session_mocker.patch.object(
        SupabaseAuthClient, "sign_in_with_password", return_value=auth_response
    )

    with TestClient(app) as client:
        response = client.post(
            url="/api/v1/login",
            data={"username": form_data.username, "password": form_data.password},
        )

        assert response.status_code == OK_STATUS_CODE


def test_sign_up(
    session_mocker: MockFixture,
    form_data: OAuth2PasswordRequestForm,
    auth_response: gotrue.AuthResponse,
) -> None:
    """
    Test the /sign_up endpoint.
    """

    session_mocker.patch.object(
        SupabaseAuthClient, "sign_up", return_value=auth_response
    )

    with TestClient(app) as client:
        response = client.post(
            url="/api/v1/sign_up",
            data={"username": form_data.username, "password": form_data.password},
        )

        assert response.status_code == OK_STATUS_CODE


def test_sign_out(
    session_mocker: MockFixture,
) -> None:
    """
    Test the /sign_out endpoint.
    """
    session_mocker.patch.object(SupabaseAuthClient, "sign_out", return_value=None)

    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/sign_out",
        )

        assert response.status_code == OK_STATUS_CODE


@pytest.fixture(scope="session")
def mock_get_user(session_mocker: MockFixture, gotrue_user: gotrue.User) -> None:
    session_mocker.patch.object(
        SupabaseAuthClient,
        "get_user",
        return_value=gotrue.UserResponse(user=gotrue_user),
    )


def test_next_records(mock_get_user: None, token: Token, record_key: RecordKey) -> None:
    """
    Test the /next_records endpoint.
    """

    headers = get_auth_header(access_token=token.access_token)

    with TestClient(app) as client:
        response = client.get(
            url=f"/api/v1/next_records/{record_key}",
            headers=headers,
        )

        assert response.status_code == OK_STATUS_CODE


def test_previous_records(mock_get_user: None, token: Token) -> None:
    """
    Test the /previous_records endpoint.
    """

    headers = get_auth_header(access_token=token.access_token)

    with TestClient(app) as client:
        response = client.get(url="/api/v1/previous_records", headers=headers)

        assert response.status_code == OK_STATUS_CODE


def test_initial_records(mock_get_user: None, token: Token) -> None:
    """
    Test the /initial_records endpoint.
    """

    headers = get_auth_header(access_token=token.access_token)

    with TestClient(app) as client:
        response = client.get(url="/api/v1/initial_records", headers=headers)
        assert response.status_code == OK_STATUS_CODE
