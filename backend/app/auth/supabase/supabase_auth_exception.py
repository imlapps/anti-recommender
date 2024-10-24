from dataclasses import dataclass

from supabase import AuthError

from app.auth import AuthException
from app.models.types import NonBlankString


@dataclass(frozen=True)
class SupabaseAuthException(AuthException):
    """A dataclass containing an Exception that was encountered in a SupabaseAuthService."""

    supabase_auth_exception: AuthError

    @property
    def message(self) -> NonBlankString:
        """The message associated with the exception."""

        return str(self.supabase_auth_exception.message)
