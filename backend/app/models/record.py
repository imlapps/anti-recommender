from pydantic import BaseModel, ConfigDict


class Record(BaseModel):
    """Pydantic Model to hold a record.
    `title` is the key of Record.
    """

    title: str
    url: str
    abstract: str | None = None

    model_config = ConfigDict(extra="allow")
