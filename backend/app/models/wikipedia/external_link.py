from pydantic import BaseModel

from app.models.types import StrippedString as ExternalLinkStringType


class ExternalLink(BaseModel):
    """Pydantic model to hold an external link of a Wikipedia Article."""

    title: ExternalLinkStringType | None = None
    link: ExternalLinkStringType | None = None
