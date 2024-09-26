from pydantic import BaseModel

from app.models.types import RecordKey


class NextRecordsQueryParams(BaseModel):
    """Pydantic Model to hold the query parameters for the /next_records endpoint."""

    record_key: RecordKey
