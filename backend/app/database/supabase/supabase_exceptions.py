from dataclasses import dataclass

from postgrest import APIError

from app.database.exceptions import DatabaseException


@dataclass(frozen=True)
class SupabaseCommandException(DatabaseException):
    supabase_command_exception: APIError | str

    @property
    def message(self) -> str:
        if isinstance(self.supabase_command_exception, APIError):
            return str(self.supabase_command_exception.message)

        return self.supabase_command_exception


@dataclass(frozen=True)
class SupabaseQueryException(DatabaseException):
    supabase_query_exception: APIError | str

    @property
    def message(self) -> str:
        if isinstance(self.supabase_query_exception, APIError):
            return str(self.supabase_query_exception.message)

        return self.supabase_query_exception
