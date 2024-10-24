from pydantic import AnyUrl, BaseModel, ConfigDict, field_validator

from app.models.types import RecordKey


class Record(BaseModel):
    """
    Pydantic model to hold a record.

    `key` is the name of a Record.

    `url` is the URL of a Record.
    """

    key: RecordKey
    url: AnyUrl

    model_config = ConfigDict(extra="allow")

    @field_validator("key")
    @classmethod
    def replace_space_with_underscore(cls, record_key: str) -> RecordKey:
        return record_key.replace(" ", "_")
