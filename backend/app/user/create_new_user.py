from typing import cast
from uuid import UUID

from app.auth.supabase import SupabaseSignInAnonymouslyResult, SupabaseUserResult
from app.auth.supabase import supabase_auth_service as auth_service
from app.models import Token
from app.user import SupabaseUserService, User


def create_new_user(token: Token) -> User:
    user_result = cast(SupabaseUserResult, auth_service.get_user(token))

    if not user_result.succeeded:
        user_id = cast(
            SupabaseSignInAnonymouslyResult, auth_service.sign_in_anonymously()
        ).user.id
    else:
        user_id = user_result.user_id

    supabase_user_service = SupabaseUserService()

    return supabase_user_service.get_user(UUID(user_id))
