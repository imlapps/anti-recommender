from pydantic import BaseModel
from app.models.types import RecordType


class CommonQueryParams(BaseModel):
    """Pydantic Model to hold the common query parameters of the API endpoints."""

    record_type: RecordType
