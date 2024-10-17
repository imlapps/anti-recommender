from pydantic import BaseModel


class TableQuery(BaseModel):
    table_name: str
    columns: str | None = None
    upsert_json: dict | tuple | None = None
    eq: dict | None = None
    constraint: str = ""
