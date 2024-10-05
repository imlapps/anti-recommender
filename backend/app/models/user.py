from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID = Field(..., alias="user_id")
