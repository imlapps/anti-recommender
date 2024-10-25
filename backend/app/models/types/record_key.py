from typing import Annotated

from pydantic import Field

# Tiny type for a Record key.
RecordKey = Annotated[
    str,
    Field(
        min_length=1,
        json_schema_extra={"strip_whitespace": "True"},
    ),
]
