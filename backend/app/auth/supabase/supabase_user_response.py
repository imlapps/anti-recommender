from dataclasses import dataclass
from uuid import UUID

import gotrue.types as gotrue

from app.auth import UserResponse
from app.models.types import UserId


@dataclass(frozen=True)
class SupabaseUserResponse(UserResponse):
    """A dataclass containing a user response from a SupabaseAuthService."""

    supabase_user_response: gotrue.UserResponse | None

    @property
    def succeeded(self) -> bool:
        """Returns True if a Supabase user response is present, and False otherwise."""

        return self.supabase_user_response is not None

    @property
    def user_id(self) -> UserId | None:
        """The user ID of the Supabase user."""

        if self.supabase_user_response:
            return UUID(self.supabase_user_response.user.id)

        return None
