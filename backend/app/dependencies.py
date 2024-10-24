from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import SecretStr

from app.auth import AuthException
from app.auth.supabase import SupabaseAuthService
from app.models import AuthToken, CredentialsError, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_authentication(
    access_token: Annotated[SecretStr, Depends(oauth2_scheme)],
) -> None:
    """
    Check if `access_token` corresponds to an authenticated `User`.

    A `CredentialsError` exception is raised if the authentication fails.
    """
    supabase_auth_service = SupabaseAuthService(settings=settings)

    try:
        supabase_auth_service.get_user(
            authentication_token=AuthToken(access_token=access_token)
        )
    except AuthException as exception:
        raise CredentialsError(
            detail=f"Could not validate credentials. Encountered exception: {exception.message}"
        ) from exception
