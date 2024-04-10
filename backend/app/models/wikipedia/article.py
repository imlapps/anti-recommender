from pydantic import ValidationInfo, field_validator

from app.models.record import Record
from app.models.wikipedia import Category, ExternalLink


class Article(Record):
    """Pydantic Model to hold the contents of a Wikipedia Article."""

    categories: tuple[Category, ...] | None = None
    external_links: tuple[ExternalLink, ...] | None = None

    @field_validator("title", "url", "abstract")
    @classmethod
    def field_must_not_contain_an_empty_string(
        cls, field: str, info: ValidationInfo
    ) -> str | None:
        """Raise error if the field contains an empty string."""
        if field.strip() == "":
            if info.field_name == "abstract":
                return None
            raise ValueError(f"{info.field_name} cannot be an empty string.")
        return field
