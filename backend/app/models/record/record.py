from pydantic import BaseModel, ConfigDict, field_validator


class Record(BaseModel):
    """Pydantic Model to hold a record."""

    model_config = ConfigDict(extra="allow")

    title: str | None = None
    abstract: str | None = None
    url: str | None = None

    @field_validator("title", "abstract", "url")
    @classmethod
    def field_must_not_contain_an_empty_string(cls, field: str) -> str | None:
        """Return None if the field contains an empty string."""
        if field.strip() == "":
            return None
        return field
