from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import SecretStr

from app.auth import AuthException
from app.models import AuthToken, CredentialsError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_authentication(
    access_token: Annotated[SecretStr, Depends(oauth2_scheme)], request: Request
) -> None:
    """
    Check if `access_token` corresponds to an authenticated `User`.

    A `CredentialsError` exception is raised if the authentication fails.
    """

    try:
        request.app.state.auth_service.get_user(
            authentication_token=AuthToken(access_token=access_token)
        )
    except AuthException as exception:
        raise CredentialsError from exception
