import gotrue.types as gotrue
import pytest
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from pytest_mock import MockFixture
from supabase import SupabaseAuthClient

from app.main import app
from app.models import Token
from app.models.types import RecordKey


def get_auth_header(access_token: str | None) -> dict[str, str]:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No access token"
        )

    return {"Authorization": f"Bearer {access_token}"}


def test_login(
    session_mocker: MockFixture,
    form_data: OAuth2PasswordRequestForm,
    auth_response: gotrue.AuthResponse,
) -> None:
    """
    Test the /login endpoint.
    """

    session_mocker.patch.object(
        SupabaseAuthClient, "sign_in_with_password", return_value=auth_response
    )

    with TestClient(app) as client:
        response = client.post(
            url="/api/v1/login",
            data={"username": form_data.username, "password": form_data.password},
        )

        assert response.status_code == status.HTTP_200_OK


def test_sign_in_anonymously() -> None:
    """
    Test the /sign_in_anonymously endpoint.
    """

    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/sign_in_anonymously",
        )

        assert response.status_code == status.HTTP_200_OK


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

        assert response.status_code == status.HTTP_200_OK


def test_sign_out() -> None:
    """
    Test the /sign_out endpoint.
    """

    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/sign_out",
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.fixture(scope="session")
def mock_get_user(session_mocker: MockFixture, gotrue_user: gotrue.User) -> None:
    session_mocker.patch.object(
        SupabaseAuthClient,
        "get_user",
        return_value=gotrue.UserResponse(user=gotrue_user),
    )


def test_next_records(
    mock_get_user: None,  # noqa: ARG001
    record_key: RecordKey,
    token: Token,
) -> None:
    """
    Test the /next_records endpoint.
    """

    headers = get_auth_header(access_token=token.access_token)

    with TestClient(app) as client:
        response = client.get(
            url=f"/api/v1/next_records/{record_key}",
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK


def test_previous_records(
    mock_get_user: None,  # noqa: ARG001
    token: Token,
) -> None:
    """
    Test the /previous_records endpoint.
    """

    headers = get_auth_header(access_token=token.access_token)

    with TestClient(app) as client:
        response = client.get(url="/api/v1/previous_records", headers=headers)

        assert response.status_code == status.HTTP_200_OK


def test_initial_records(
    mock_get_user: None,  # noqa: ARG001
    token: Token,
) -> None:
    """
    Test the /initial_records endpoint.
    """

    headers = get_auth_header(access_token=token.access_token)

    with TestClient(app) as client:
        response = client.get(url="/api/v1/initial_records", headers=headers)
        assert response.status_code == status.HTTP_200_OK
