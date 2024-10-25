from pydantic import BaseModel

from app.models.types import StrippedString as CategoryStringType


class Category(BaseModel):
    """Pydantic model to hold a category of a Wikipedia Article."""

    text: CategoryStringType | None = None
    link: CategoryStringType | None = None
