from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth import AuthException
from app.auth.supabase import supabase_auth_service as auth_service
from app.models import CredentialsError, AuthToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_authentication(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """
    Check if `access_token` corresponds to an authenticated `User`.

    A `CredentialsError` exception is raised if the authentication fails.
    """
    try:
        auth_service.get_user(authentication_token=AuthToken(access_token=access_token))
    except AuthException as exception:
        raise CredentialsError(
            detail=f"Could not validate credentials. Encountered exception: {exception.message}"
        ) from exception
