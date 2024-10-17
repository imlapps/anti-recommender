from dataclasses import dataclass

from gotrue.types import AuthResponse, UserResponse, User

from app.auth import AuthResult, UserResult
from app.models import Token


@dataclass(frozen=True)
class SupabaseSignUpResult(AuthResult):
    supabase_sign_up_result: AuthResponse

    @property
    def succeeded(self) -> bool:
        return (
            self.supabase_sign_up_result.user is not None
            and self.supabase_sign_up_result.session is not None
        )

    @property
    def authentication_token(self) -> Token:
        return Token(**self.supabase_sign_up_result.session.model_dump())


@dataclass(frozen=True)
class SupabaseSignInResult(AuthResult):
    supabase_sign_in_result: AuthResponse

    @property
    def succeeded(self) -> bool:
        return (
            self.supabase_sign_in_result.user is not None
            and self.supabase_sign_in_result.session is not None
        )

    @property
    def authentication_token(self) -> Token:
        return Token(**self.supabase_sign_in_result.session.model_dump())


@dataclass(frozen=True)
class SupabaseSignInAnonymouslyResult(AuthResult):
    supabase_sign_in_anonymously_result: AuthResponse

    @property
    def succeeded(self) -> bool:
        return (
            self.supabase_sign_in_anonymously_result.user is not None
            and self.supabase_sign_in_anonymously_result.session is not None
        )

    @property
    def authentication_token(self) -> Token:
        return Token(**self.supabase_sign_in_anonymously_result.session.model_dump())

    @property
    def user(self) -> User:
        return self.supabase_sign_in_anonymously_result.user


@dataclass(frozen=True)
class SupabaseSignOutResult(AuthResult):
    supabase_sign_out_result: AuthResponse

    @property
    def succeeded(self) -> bool:
        return self.supabase_sign_out_result.session is None

    @property
    def authentication_token(self) -> Token:
        if self.supabase_sign_out_result.session:
            return Token(**self.supabase_sign_out_result.session.model_dump())

        return Token(access_token="")


@dataclass(frozen=True)
class SupabaseUserResult(UserResult):
    supabase_user_result: UserResponse | None

    @property
    def succeeded(self) -> bool:
        return self.supabase_user_result and self.supabase_user_result.user is not None

    @property
    def user_id(self) -> str:
        return str(self.supabase_user_result.user.id)
