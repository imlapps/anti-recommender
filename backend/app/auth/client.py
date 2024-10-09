import supabase
from app.models import settings
from gotrue.types import (
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
            return cast(Client, supabase.create_client()).auth

    def sign_in(
        self, *, credentials: SignInWithEmailAndPasswordCredentials
    ) -> AuthResponse | None:
        """Log in an existing user with email and password credentials."""

        if isinstance(self.__auth_client, SupabaseAuthClient):
            return self.__auth_client.sign_in_with_password(**credentials)

        return None

    def sign_out(self) -> None:
        """Sign out from all sessions that a user has signed in to."""

        if isinstance(self.__auth_client, SupabaseAuthClient):
            self.__auth_client.sign_out()
        return None

    def sign_up(self, *, credentials: SignUpWithEmailAndPasswordCredentials) -> None:
        """Sign up a user with email and password credentials."""

        if isinstance(self.__auth_client, SupabaseAuthClient):
            return self.__auth_client.sign_up(**credentials)
