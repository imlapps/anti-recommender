from pydantic import BaseModel, field_validator


class AntiRecommendation(BaseModel):
    """Pydantic Model to hold an anti-recommendation."""

    title: str = ""
    url: str = ""

    @field_validator("title",  "url")
    @classmethod
    def field_must_not_contain_an_empty_string(cls, field: str) -> str | None:
        """Return None if the field contains an empty string."""
        if field.strip() == "":
            return None
        return field
