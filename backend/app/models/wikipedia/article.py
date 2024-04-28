from pydantic import Field

from typing import Annotated

from app.models.record import Record
from app.models.types import RecordKey
from app.models.wikipedia.category import Category
from app.models.wikipedia.external_link import ExternalLink


class Article(Record):
    """Pydantic Model to hold the contents of a Wikipedia Article."""

    key: RecordKey = Field(..., alias="title")

    abstract: (
        Annotated[str, Field(json_schema_extra={"strip_whitespace": "True"})] | None
    ) = None
    categories: tuple[Category, ...] | None = None
    external_links: tuple[ExternalLink, ...] | None = None
