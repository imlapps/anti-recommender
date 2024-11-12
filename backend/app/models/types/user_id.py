from typing import Annotated
from uuid import UUID

from pydantic import Field
from pydantic.types import UuidVersion

"""
Tiny type for a User's Id.

`UserId` is a version 4 UUID.
"""
UserId = Annotated[UUID, Field(..., alias="user_id"), UuidVersion(4)]
