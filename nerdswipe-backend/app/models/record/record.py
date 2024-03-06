from pydantic import BaseModel


class Record(BaseModel):
    """Pydantic Model to hold a Wikipedia record."""

    class AbstractInfo(BaseModel):
        title: str = ""
        abstract: str = ""
        url: str = ""

    class Categories(BaseModel):
        text: str = ""
        link: str = ""

    class ExternalLink(BaseModel):
        title: str = ""
        link: str = ""

    abstract_info: AbstractInfo = AbstractInfo()
    categories: tuple[Categories, ...] | None = None
    externallinks: tuple[ExternalLink, ...] | None = None
