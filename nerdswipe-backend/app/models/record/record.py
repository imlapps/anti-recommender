from pydantic import BaseModel


class AbstractInfo(BaseModel):
    """Pydantic Model that holds the Abstract Information of a Wikipedia Article."""

    title: str = ""
    abstract: str = ""
    url: str = ""


class Categories(BaseModel):
    """Pydantic Model to hold a category of a Wikipedia Article."""

    text: str = ""
    link: str = ""


class ExternalLink(BaseModel):
    """Pydantic Model to hold an external link of a Wikipedia Article."""

    title: str = ""
    link: str = ""


class Record(BaseModel):
    """Pydantic Model to hold a record."""

    abstract_info: AbstractInfo | None = None
    categories: tuple[Categories, ...] | None = None
    externallinks: tuple[ExternalLink, ...] | None = None
