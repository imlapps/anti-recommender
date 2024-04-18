from pydantic import BaseModel, ConfigDict


class Record(BaseModel):
    """Pydantic Model to hold a record.
    `key` is the name of Record.
    `url` is the URL of the Record.
    """

    key: str
    url: str

    model_config = ConfigDict(extra="allow")
