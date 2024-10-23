import gotrue.types as gotrue
import pytest
from fastapi import FastAPI, status
from fastapi.security import OAuth2PasswordRequestForm
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockFixture
from supabase import SupabaseAuthClient

from app.models.types import RecordKey


@pytest.mark.anyio(loop_scope="session")
async def test_login(
    app: FastAPI,
    auth_response: gotrue.AuthResponse,
    form_data: OAuth2PasswordRequestForm,
    mock_get_user: None,  # noqa: ARG001
    session_mocker: MockFixture,
) -> None:
    """
    Test the /login endpoint.
    """

    session_mocker.patch.object(
        SupabaseAuthClient, "sign_in_with_password", return_value=auth_response
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.post(
            url="/api/v1/login",
            data={"username": form_data.username, "password": form_data.password},
        )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio(loop_scope="session")
async def test_sign_in_anonymously(app: FastAPI) -> None:
    """
    Test the /sign_in_anonymously endpoint.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.get(
            url="/api/v1/sign_in_anonymously",
        )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio(loop_scope="session")
async def test_sign_up(
    app: FastAPI,
    auth_response: gotrue.AuthResponse,
    form_data: OAuth2PasswordRequestForm,
    mock_get_user: None,  # noqa: ARG001
    session_mocker: MockFixture,
) -> None:
    """
    Test the /sign_up endpoint.
    """

    session_mocker.patch.object(
        SupabaseAuthClient, "sign_up", return_value=auth_response
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.post(
            url="/api/v1/sign_up",
            data={"username": form_data.username, "password": form_data.password},
        )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio(loop_scope="session")
async def test_sign_out(app: FastAPI) -> None:
    """
    Test the /sign_out endpoint.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.get(
            url="/api/v1/sign_out",
        )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio(loop_scope="session")
async def test_next_records(
    app: FastAPI,
    auth_header: dict[str, str],
    mock_get_user: None,  # noqa: ARG001
    record_key: RecordKey,
) -> None:
    """
    Test the /next_records endpoint.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.get(
            url=f"/api/v1/next_records/{record_key}",
            headers=auth_header,
        )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio(loop_scope="session")
async def test_previous_records(
    app: FastAPI,
    auth_header: dict[str, str],
    mock_get_user: None,  # noqa: ARG001
) -> None:
    """
    Test the /previous_records endpoint.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.get(url="/api/v1/previous_records", headers=auth_header)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio(loop_scope="session")
async def test_initial_records(
    app: FastAPI,
    auth_header: dict[str, str],
    mock_get_user: None,  # noqa: ARG001
) -> None:
    """
    Test the /initial_records endpoint.
    """

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.nerdswipe.com"
    ) as client:
        response = await client.get(url="/api/v1/initial_records", headers=auth_header)

    assert response.status_code == status.HTTP_200_OK
