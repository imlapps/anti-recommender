import supabase
from app.models import settings
from gotrue.types import (
    UserResponse,
    AuthResponse,
    SignInWithEmailAndPasswordCredentials,
    SignUpWithEmailAndPasswordCredentials,
)
from supabase import SupabaseAuthClient, Client
from typing import cast


class AuthClient:
    """An authentication and authorization client class"""

    def __init__(self) -> None:
        self.__auth_client: SupabaseAuthClient | None = self.__select_auth_client()

    def __select_auth_client(self) -> SupabaseAuthClient | None:
        """
        Create and return an authentication client.

        A `SupabaseAuthClient` instance is returned if the required parameters are in `settings`.
        """

        if settings.supabase_url and settings.supabase_key:
            return cast(
                Client,
                supabase.create_client(
                    supabase_url=settings.supabase_url,
                    supabase_key=settings.supabase_key,
                ),
            ).auth

        return None

    def sign_in(
        self, credentials: SignInWithEmailAndPasswordCredentials
    ) -> AuthResponse | None:
        """Log in an existing user with email and password credentials."""

        if isinstance(self.__auth_client, SupabaseAuthClient):
            return self.__auth_client.sign_in_with_password(**credentials)

        return None

    def sign_out(self) -> None:
        """Sign out from all sessions that a user has signed in to."""

        if isinstance(self.__auth_client, SupabaseAuthClient):
            self.__auth_client.sign_out()

    def sign_up(
        self, credentials: SignUpWithEmailAndPasswordCredentials
    ) -> AuthResponse | None:
        """Sign up a user with email and password credentials."""

        if isinstance(self.__auth_client, SupabaseAuthClient):
            return self.__auth_client.sign_up(**credentials)

        return None

    def get_user(self, jwt: str | None = None) -> UserResponse | None:
        """
        Return the current user if there there is an existing session.

        Takes in an optional access token `jwt`.
        """

        if isinstance(self.__auth_client, SupabaseAuthClient):
            return self.__auth_client.get_user(jwt=jwt)

        return None


auth_client = AuthClient()
