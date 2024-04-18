from pydantic import BaseModel, ConfigDict


class Record(BaseModel):
    """Pydantic Model to hold a record.
    `key` is the name of a Record.
    `url` is the URL of a Record.
    """

    key: str
    url: str

    model_config = ConfigDict(extra="allow")
