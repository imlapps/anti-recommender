from pydantic import BaseModel


class AntiRecommendation(BaseModel):
    """Pydantic Model to hold an anti-recommendation record."""

    title: str = ""
    url: str = ""
