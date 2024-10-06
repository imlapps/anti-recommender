from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    """
    Pydantic model that contains information of a User.

    `id` is the UUID of the User.
    """

    id: UUID = Field(..., alias="user_id")
