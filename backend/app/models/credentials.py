from typing import TypedDict

from pydantic import EmailStr, SecretStr


class Credentials(TypedDict):
    """A TypedDict containing parameters used for User authentication."""

    email: EmailStr
    password: SecretStr
