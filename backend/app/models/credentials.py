from typing import TypedDict

from pydantic import EmailStr, SecretStr


class Credentials(TypedDict):
    email: EmailStr
    password: SecretStr
