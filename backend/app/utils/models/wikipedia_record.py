from pydantic import BaseModel 
from typing import List, Dict, Tuple

class WikipediaRecord(BaseModel):
    """A Pydantic Model to contain Wikipedia Abstracts"""

    class AbstractInfo(BaseModel):
        title: str = ""
        abstract: str = ""
        url: str = ""

    class Sublink(BaseModel):
        anchor: str = ""
        link: str = ""

    class Categories(BaseModel):
        text: str = ""
        link: str = ""

    class ExternalLink(BaseModel):
        title: str = ""
        link: str = ""

    abstract_info: AbstractInfo = AbstractInfo()
    sublinks: List[Sublink] = []
    categories: List[Categories] = []
    externallinks: List[ExternalLink] = []