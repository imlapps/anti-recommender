from fastapi.testclient import TestClient

from app.main import app

OK_STATUS_CODE = 200


def test_next_records(record_key: str) -> None:
    """
    Test the /next_records endpoint.
    """
    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/next_records",
            params={"record_key": record_key},
        )

        assert response.status_code == OK_STATUS_CODE


def test_previous_records() -> None:
    """
    Test the /previous_records endpoint.
    """

    with TestClient(app) as client:
        response = client.get(url="/api/v1/previous_records")
        assert response.status_code == OK_STATUS_CODE


def test_initial_records() -> None:
    """
    Test the /initial_records endpoint.
    """

    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/initial_records",
        )
        assert response.status_code == OK_STATUS_CODE
