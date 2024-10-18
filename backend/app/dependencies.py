from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth import UserException, UserResult
from app.auth.supabase import supabase_auth_service as auth_service
from app.models import CredentialsError, Token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_authentication(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """
    Check if `access_token` corresponds to an authenticated `User`.

    A `CredentialsError` exception is raised if the authentication fails.
    """
    try:
        user_result: UserResult = auth_service.get_user(
            authentication_token=Token(access_token=access_token)
        )
    except UserException as exception:
        raise CredentialsError(
            detail=f"Could not validate credentials. Encountered exception: {exception.message}"
        ) from exception

    if not user_result.succeeded:
        raise CredentialsError(
            detail="Could not validate credentials. Check that the access token is correct."
        ) from None
