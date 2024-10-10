from uuid import UUID

from pydantic import BaseModel, Field

from app.models.types import RecordKey


class User(BaseModel):
    """
    Pydantic model that contains information of a User.

    `id` is the UUID of the User.
    """

    id: UUID = Field(..., alias="user_id")
    record_key: RecordKey | None = None
