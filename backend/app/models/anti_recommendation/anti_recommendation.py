from pydantic import BaseModel


class AntiRecommendation(BaseModel):
    """Pydantic Model to hold an anti-recommendation."""

    title: str = ""
    url: str = ""
