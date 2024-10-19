from dataclasses import dataclass

from supabase import AuthError, AuthInvalidCredentialsError

from app.auth import AuthInvalidCredentialsException, UserException


@dataclass(frozen=True)
class SupabaseUserException(UserException):
    supabase_user_exception: AuthError

    @property
    def message(self) -> str:
        return str(self.supabase_user_exception.message)


@dataclass(frozen=True)
class SupabaseAuthInvalidCredentialsException(AuthInvalidCredentialsException):
    supabase_auth_exception: AuthInvalidCredentialsError

    @property
    def message(self) -> str:
        return str(self.supabase_auth_exception.message)
