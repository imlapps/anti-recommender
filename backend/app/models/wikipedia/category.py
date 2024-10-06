from typing import Annotated

from pydantic import BaseModel, Field

# A custom data type for str fields in Category
CategoryStringType = Annotated[
    str, Field(json_schema_extra={"strip_whitespace": "True"})
]


class Category(BaseModel):
    """Pydantic model to hold a category of a Wikipedia Article."""

    text: CategoryStringType | None = None
    link: CategoryStringType | None = None
