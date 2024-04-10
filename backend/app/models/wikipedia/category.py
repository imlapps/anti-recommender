from pydantic import BaseModel


class Category(BaseModel):
    """Pydantic Model to hold a category of a Wikipedia Article."""

    text: str | None = None
    link: str | None = None
