from pydantic import BaseModel


class ExternalLink(BaseModel):
    """Pydantic Model to hold an external link of a Wikipedia Article."""

    title: str | None = None
    link: str | None = None
