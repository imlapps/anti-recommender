from typing import override

import supabase
from supabase import AuthError, AuthInvalidCredentialsError, SupabaseAuthClient

from app.auth import AuthException, AuthService, UserNotFoundAuthException
from app.auth.supabase import SupabaseAuthResponse, SupabaseUserResponse
from app.models import AuthToken, Credentials, Settings


class SupabaseAuthService(AuthService):
    """
    A concrete implementation of AuthService.

    A SupabaseAuthService uses Supabase Auth to authenticate a User.
    """

    def __init__(self, *, settings: Settings):
        self.__auth_client = self.__create_client(settings=settings)

    @staticmethod
    def __create_client(*, settings: Settings) -> SupabaseAuthClient:
        """Return a Supabase auth client, if Supabase URL and Supabase key are present in Settings."""

        if settings.supabase_key and settings.supabase_url:
            return supabase.create_client(
                supabase_url=str(settings.supabase_url),
                supabase_key=settings.supabase_key.get_secret_value(),
            ).auth
        msg = "Cannot use Supabase Auth without Supabase URL and Supabase key."
        raise AuthException(msg)

    @override
    def get_user(self, *, authentication_token: AuthToken) -> SupabaseUserResponse:
        """
        Return a SupabaseUserResponse containing a Supabase user that corresponds to authentication_token.
        """

        try:
            supabase_user_result = self.__auth_client.get_user(
                authentication_token.access_token.get_secret_value()
            )
        except AuthError as exception:
            raise AuthException from exception

        if not supabase_user_result:
            raise UserNotFoundAuthException

        return SupabaseUserResponse(supabase_user_result)

    @override
    def sign_in(
        self, *, authentication_credentials: Credentials
    ) -> SupabaseAuthResponse:
        """Sign in to Supabase Auth with authentication_credentials."""

        try:
            supabase_sign_in_result = self.__auth_client.sign_in_with_password(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise AuthException from exception

        return SupabaseAuthResponse(supabase_sign_in_result)

    @override
    def sign_in_anonymously(
        self,
    ) -> SupabaseAuthResponse:
        """Sign in anonymously to Supabase Auth."""

        try:
            supabase_sign_in_anonymously_result = (
                self.__auth_client.sign_in_anonymously()
            )
        except AuthInvalidCredentialsError as exception:
            raise AuthException from exception

        return SupabaseAuthResponse(supabase_sign_in_anonymously_result)

    @override
    def sign_up(
        self, *, authentication_credentials: Credentials
    ) -> SupabaseAuthResponse:
        """Sign up for Supabase Auth with authentication_credentials."""

        try:
            supabase_sign_up_result = self.__auth_client.sign_up(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise AuthException from exception

        return SupabaseAuthResponse(supabase_sign_up_result)

    @override
    def sign_out(self) -> None:
        """Sign out from Supabase Auth."""

        try:
            self.__auth_client.sign_out()
        except AuthError as exception:
            raise AuthException from exception
