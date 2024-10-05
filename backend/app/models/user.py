from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(..., alias="user_id")
