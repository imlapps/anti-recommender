from typing import override

import supabase
from gotrue.types import AuthResponse
from supabase import (
    AuthError,
    AuthInvalidCredentialsError,
    SupabaseAuthClient,
)

from app.auth import AuthService
from app.auth.supabase import SupabaseAuthException, SupabaseAuthResponse
from app.models import AuthToken, Credentials, Settings


class SupabaseAuthService(AuthService):
    def __init__(self, settings: Settings):
        self.__auth_client: SupabaseAuthClient = supabase.create_client(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key,
        ).auth

    @override
    def get_user(self, authentication_token: AuthToken) -> SupabaseAuthResponse:
        try:
            supabase_user_result = self.__auth_client.get_user(
                authentication_token.access_token
            )
        except AuthError as exception:
            raise SupabaseAuthException(exception) from exception

        if not supabase_user_result.user:
            return self.sign_in_anonymously()

        return SupabaseAuthResponse(AuthResponse(user=supabase_user_result.user))

    @override
    def sign_in(self, authentication_credentials: Credentials) -> SupabaseAuthResponse:
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
        try:
            supabase_sign_in_anonymously_result = (
                self.__auth_client.sign_in_anonymously()
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthException(exception) from exception

        return SupabaseAuthResponse(supabase_sign_in_anonymously_result)

    @override
    def sign_up(self, authentication_credentials: Credentials) -> SupabaseAuthResponse:
        try:
            supabase_sign_out_result = self.__auth_client.sign_up(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthException(exception) from exception

        return SupabaseAuthResponse(supabase_sign_out_result)

    @override
    def sign_out(self) -> SupabaseAuthResponse:
        self.__auth_client.sign_out()

        return SupabaseAuthResponse(
            AuthResponse(session=self.__auth_client.get_session())
        )
