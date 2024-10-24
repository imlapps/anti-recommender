from pydantic import BaseModel
from pydantic.types import SecretStr


class AuthToken(BaseModel):
    access_token: SecretStr
    refresh_token: SecretStr | None = None
    token_type: str = "Bearer"
