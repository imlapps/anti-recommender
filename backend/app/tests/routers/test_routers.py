from fastapi.testclient import TestClient

from app.main import app
from app.models.types.record_type import RecordType

OK_STATUS_CODE = 200


def test_next_records(record_key: str, record_type: RecordType) -> None:
    """
    Test the /next_records endpoint.
    """
    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/nerdswipe/next_records",
            params={"record_key": record_key, "record_type": record_type.value},
        )

        assert response.status_code == OK_STATUS_CODE


def test_previous_records() -> None:
    """
    Test the /previous_records endpoint.
    """

    with TestClient(app) as client:
        response = client.get(url="/api/v1/nerdswipe/previous_records")
        assert response.status_code == OK_STATUS_CODE


def test_initial_records(record_type: RecordType) -> None:
    """
    Test the /initial_records endpoint.
    """

    with TestClient(app) as client:
        response = client.get(
            url="/api/v1/nerdswipe/initial_records",
            params={"record_type": record_type.value},
        )
        assert response.status_code == OK_STATUS_CODE
