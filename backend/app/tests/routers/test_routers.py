from fastapi.testclient import TestClient
from app.main import app


def test_next(record_key: str, record_type: str) -> None:
    """
    Test the /next endpoint.
    """
    with TestClient(app) as client:
        response = client.get(
            url="/ap1/v1/nerdswipe/next",
            params={"record_key": record_key, "record_type": record_type},
        )

        assert response.status_code == 200


def test_previous() -> None:
    """
    Test the /previous endpoint.
    """

    with TestClient(app) as client:
        response = client.get(url="/ap1/v1/nerdswipe/previous")
        assert response.status_code == 200


def test_current(record_type: str) -> None:
    """
    Test the /current endpoint.
    """

    with TestClient(app) as client:
        response = client.get(
            url="/ap1/v1/nerdswipe/current", params={"record_type": record_type}
        )
        assert response.status_code == 200
