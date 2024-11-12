from typing import Literal

from pydantic import BaseModel
from pydantic.types import SecretStr


class AuthToken(BaseModel):
    """A Pydantic model that contains parameters for an authentication token."""

    access_token: SecretStr
    refresh_token: SecretStr | None = None
    token_type: Literal["Bearer"] = "Bearer"
