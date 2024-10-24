from dataclasses import dataclass
from uuid import UUID

import gotrue.types as gotrue

from app.auth import AuthResponse
from app.models import AuthToken


@dataclass(frozen=True)
class SupabaseAuthResponse(AuthResponse):
    """A dataclass containing an authentication response from a SupabaseAuthService."""

    supabase_auth_response: gotrue.AuthResponse

    @property
    def authenticated_user(self) -> gotrue.User:
        """The authenticated Supabase user."""

        return self.supabase_auth_response.user

    @property
    def user_id(self) -> UUID:
        """The user ID of the authenticated Supabase user."""

        return UUID(self.supabase_auth_response.user.id)

    @property
    def authentication_token(self) -> AuthToken:
        """A new AuthToken containing parameters from an authenticated Supabase user."""

        return AuthToken(**self.supabase_auth_response.session.model_dump())
