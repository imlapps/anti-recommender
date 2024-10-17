from typing import override

import supabase
from gotrue.types import AuthResponse
from supabase import AuthError, AuthInvalidCredentialsError, SupabaseAuthClient

from app.auth import AuthResult, AuthService, UserResult
from app.auth.supabase import (
    SupabaseAuthInvalidCredentialsException,
    SupabaseSignInResult,
    SupabaseSignOutResult,
    SupabaseSignUpResult,
    SupabaseSignInAnonymouslyResult,
    SupabaseUserException,
    SupabaseUserResult,
)
from app.models import Credentials, Token, settings


class SupabaseAuthService(AuthService):
    def __init__(self):
        self.__auth_client: SupabaseAuthClient = supabase.create_client(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key,
        ).auth

    @override
    def get_user(self, authentication_token: Token) -> UserResult:
        try:
            supabase_user_result = self.__auth_client.get_user(
                authentication_token.access_token
            )
        except AuthError as exception:
            raise SupabaseUserException(exception) from exception

        return SupabaseUserResult(supabase_user_result)

    @override
    def sign_in(self, authentication_credentials: Credentials) -> AuthResult:
        try:
            supabase_sign_in_result = self.__auth_client.sign_in_with_password(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthInvalidCredentialsException(exception) from exception

        return SupabaseSignInResult(supabase_sign_in_result)

    @override
    def sign_in_anonymously(
        self,
    ) -> AuthResult:
        try:
            supabase_sign_in_anonymously_result = (
                self.__auth_client.sign_in_anonymously()
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthInvalidCredentialsException(exception) from exception

        return SupabaseSignInAnonymouslyResult(supabase_sign_in_anonymously_result)

    @override
    def sign_up(self, authentication_credentials: Credentials) -> AuthResult:
        try:
            supabase_sign_out_result = self.__auth_client.sign_up(
                **authentication_credentials
            )
        except AuthInvalidCredentialsError as exception:
            raise SupabaseAuthInvalidCredentialsException(exception) from exception

        return SupabaseSignUpResult(supabase_sign_out_result)

    @override
    def sign_out(self) -> AuthResult:
        self.__auth_client.sign_out()

        return SupabaseSignOutResult(
            AuthResponse(session=self.__auth_client.get_session())
        )


supabase_auth_service = SupabaseAuthService()
