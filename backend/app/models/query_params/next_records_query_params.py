from app.models.query_params.common_query_params import CommonQueryParams
from app.models.types import RecordKey


class NextRecordsQueryParams(CommonQueryParams):
    """Pydantic Model to hold the query parameters for the /next_records endpoint."""

    record_key: RecordKey
