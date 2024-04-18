from app.models.types import RecordType


def next_records_parameters(
    record_key: str, record_type: RecordType
) -> dict[str, str | RecordType]:
    """Return parameters for the next_records endpoint."""

    return {"record_key": record_key, "record_type": record_type}
