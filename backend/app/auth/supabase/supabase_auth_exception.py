from dataclasses import dataclass

from supabase import AuthError

from app.auth import AuthException


@dataclass(frozen=True)
class SupabaseAuthException(AuthException):
    supabase_auth_exception: AuthError

    @property
    def message(self) -> str:
        return str(self.supabase_auth_exception.message)
