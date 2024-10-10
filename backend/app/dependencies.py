from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from postgrest import APIError

from app.auth import auth_client
from app.models import CredentialsError, User, UserState
from app.utils import fetch_user_state_from_database

if TYPE_CHECKING:
    from gotrue.types import AuthResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_authentication(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> UserState:
    """
    Check if `access_token` corresponds to an authenticated `User`.

    Return a `User` with an authenticated `UUID`.
    """
    try:
        user_response: AuthResponse | None = auth_client.get_user(jwt=str(access_token))
    except APIError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to check user authentication. Encountered APIError with exception: {exception}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception

    if not user_response:
        raise CredentialsError(detail="Could not validate credentials")

    return fetch_user_state_from_database(user=User(user_id=user_response.user.id))
