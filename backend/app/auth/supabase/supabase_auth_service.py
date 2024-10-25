from typing import override

import supabase
from gotrue.types import AuthResponse
from supabase import AuthError, AuthInvalidCredentialsError, SupabaseAuthClient

from app.auth import AuthService
from app.auth.supabase import SupabaseAuthException, SupabaseAuthResponse
from app.models import AuthToken, Credentials, Settings


class SupabaseAuthService(AuthService):
    """
    A concrete implementation of `AuthService`.

    A `SupabaseAuthService` uses Supabase Auth to authenticate a `User`.
    """

    def __init__(self, settings: Settings):
        self.__auth_client = self.__create_client(settings)

    @staticmethod
    def __create_client(settings: Settings) -> SupabaseAuthClient:
        if not settings.supabase_key and not settings.supabase_url:
            raise SupabaseAuthException

        return supabase.create_client(
            supabase_url=str(settings.supabase_url),
            supabase_key=settings.supabase_key.get_secret_value(),
        ).auth

    @override
    def get_user(self, authentication_token: AuthToken) -> SupabaseAuthResponse:
        """
        Return a SupabaseAuthResponse containing a Supabase user that corresponds to `authentication_token`.

        If no such user is found, invoke SupabaseAuthService.sign_in_anonymously.
        """
        try:
            supabase_user_result = self.__auth_client.get_user(
                authentication_token.access_token.get_secret_value()
            )
        except AuthError as exception:
            raise SupabaseAuthException(exception) from exception

        if not supabase_user_result.user:
            return self.sign_in_anonymously()

        return SupabaseAuthResponse(AuthResponse(user=supabase_user_result.user))

    @override
    def sign_in(self, authentication_credentials: Credentials) -> SupabaseAuthResponse:
        """Sign in to Supabase Auth, and return a SupabaseAuthResponse containing a Supabase user."""

        try:
            supabase_sign_in_result = self.__auth_client.sign_in_with_password(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthException(exception) from exception

        return SupabaseAuthResponse(supabase_sign_in_result)

    @override
    def sign_in_anonymously(
        self,
    ) -> SupabaseAuthResponse:
        """Sign in anonymously to Supabase Auth, and return a SupabaseAuthResponse containing a new Supabase user."""

        try:
            supabase_sign_in_anonymously_result = (
                self.__auth_client.sign_in_anonymously()
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthException(exception) from exception

        return SupabaseAuthResponse(supabase_sign_in_anonymously_result)

    @override
    def sign_up(self, authentication_credentials: Credentials) -> SupabaseAuthResponse:
        """Sign up for Supabase Auth, and return a SupabaseAuthResponse containing a new Supabase user."""

        try:
            supabase_sign_up_result = self.__auth_client.sign_up(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthException(exception) from exception

        return SupabaseAuthResponse(supabase_sign_up_result)

    @override
    def sign_out(self) -> SupabaseAuthResponse:
        """Sign out from Supabase Auth."""

        self.__auth_client.sign_out()

        return SupabaseAuthResponse(
            AuthResponse(session=self.__auth_client.get_session())
        )
