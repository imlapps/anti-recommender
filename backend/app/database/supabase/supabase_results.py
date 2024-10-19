from dataclasses import dataclass

from postgrest import APIResponse

from app.database import CommandResult, QueryResult


@dataclass(frozen=True)
class SupabaseDeleteQueryResult(CommandResult):
    supabase_delete_query_result: APIResponse

    @property
    def succeeded(self) -> bool:
        return len(self.supabase_delete_query_result.data) > 0


@dataclass(frozen=True)
class SupabaseUpsertQueryResult(CommandResult):
    supabase_upsert_query_result: APIResponse

    @property
    def succeeded(self) -> bool:
        return len(self.supabase_upsert_query_result.data) > 0


@dataclass(frozen=True)
class SupabaseFetchQueryResult(QueryResult):
    supabase_fetch_query_result: APIResponse

    @property
    def succeeded(self) -> bool:
        return len(self.supabase_fetch_query_result.data) > 0

    @property
    def data(self) -> tuple:
        return tuple(self.supabase_fetch_query_result.data)
