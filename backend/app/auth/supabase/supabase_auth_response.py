from dataclasses import dataclass
from uuid import UUID

import gotrue.types as gotrue

from app.auth import AuthResponse
from app.models import AuthToken


@dataclass(frozen=True)
class SupabaseAuthResponse(AuthResponse):
    supabase_auth_response: gotrue.AuthResponse

    @property
    def authenticated_user(self) -> gotrue.User:
        return self.supabase_auth_response.user

    @property
    def user_id(self) -> UUID:
        return UUID(self.supabase_auth_response.user.id)

    @property
    def authentication_token(self) -> AuthToken:
        return AuthToken(**self.supabase_auth_response.session.model_dump())
