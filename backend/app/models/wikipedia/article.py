from typing import Annotated

from pydantic import Field

from app.models import Record
from app.models.types import RecordKey
from app.models.wikipedia import Category, ExternalLink


class Article(Record):
    """Pydantic model to hold the contents of a Wikipedia Article."""

    key: RecordKey = Field(..., alias="title")

    abstract: (
        Annotated[str, Field(json_schema_extra={"strip_whitespace": "True"})] | None
    ) = None
    categories: tuple[Category, ...] | None = None
    external_links: tuple[ExternalLink, ...] | None = None
