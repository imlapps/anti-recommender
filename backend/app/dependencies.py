from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth import UserException, UserResult
from app.auth.supabase import supabase_auth_service as auth_service
from app.models import CredentialsError, Token, User, UserState
from app.utils import fetch_user_state_from_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_authentication(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> UserState:
    """
    Check if `access_token` corresponds to an authenticated `User`.

    Return a `User` with an authenticated `UUID`.
    """
    try:
        user_result: UserResult = auth_service.get_user(
            authentication_token=Token(access_token=access_token)
        )
    except UserException:
        raise CredentialsError(detail="Could not validate credentials") from None

    return fetch_user_state_from_database(user=User(user_id=UUID(user_result.user_id)))
