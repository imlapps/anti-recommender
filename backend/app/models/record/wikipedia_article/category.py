from pydantic import BaseModel, field_validator


class Category(BaseModel):
    """Pydantic Model to hold a category of a Wikipedia Article."""

    text: str | None = None
    link: str | None = None

    @field_validator("text", "link")
    @classmethod
    def field_must_not_contain_an_empty_string(cls, field: str) -> str | None:
        """Return None if the field contains an empty string."""
        if field.strip() == "":
            return None
        return field
