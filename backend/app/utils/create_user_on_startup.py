from uuid import UUID
from app.user import SupabaseUserService, User

from app.auth.supabase import supabase_auth_service as auth_service
from app.models import Token
from app.auth.supabase import SupabaseSignInAnonymouslyResult, SupabaseUserResult


from typing import cast


def create_user_on_startup() -> User:

    user_result = cast(
        SupabaseUserResult, auth_service.get_user(Token(access_token=""))
    )

    if not user_result.succeeded:
        user_id = cast(
            SupabaseSignInAnonymouslyResult, auth_service.sign_in_anonymously()
        ).user.id
    else:
        user_id = user_result.user_id

    supabase_user_service = SupabaseUserService()

    return supabase_user_service.get_user(UUID(user_id))
