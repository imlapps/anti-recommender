from dataclasses import dataclass
from typing import Union

import gotrue.types as gotrue

from app.auth import AuthResponse
from app.models import AuthToken


@dataclass(frozen=True)
class SupabaseAuthResponse(AuthResponse):
    supabase_auth_response: gotrue.AuthResponse

    @property
    def authenticated_user(self) -> Union[gotrue.User, None]:
        return self.supabase_auth_response.user

    @property
    def authentication_token(self) -> AuthToken:
        return AuthToken(**self.supabase_auth_response.session.model_dump())
