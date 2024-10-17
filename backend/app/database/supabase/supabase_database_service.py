import supabase
from postgrest import APIError
from supabase import Client

from app.database import DatabaseService
from app.database.results import CommandResult, QueryResult
from app.database.supabase import (
    SupabaseCommandException,
    SupabaseDeleteQueryResult,
    SupabaseFetchQueryResult,
    SupabaseQueryException,
    SupabaseUpsertQueryResult,
)
from app.models import settings
from app.models.table_query import TableQuery


class SupabaseDatabaseService(DatabaseService):
    def __init__(self) -> None:
        self.__database_client: Client = supabase.create_client(
            settings.supabase_url, settings.supabase_key
        )

    def command(self, table_query: TableQuery) -> CommandResult:
        if table_query.eq:
            return self.__delete(**table_query.model_dump())

        if not table_query.upsert_json:
            raise SupabaseCommandException(
                supabase_command_exception="Invalid command parameters."
            ) from None

        return self.__upsert(**table_query.model_dump())

    def query(self, table_query: TableQuery) -> QueryResult:
        if not table_query.columns:
            raise SupabaseQueryException(
                supabase_query_exception="Invalid query parameters. Missing columns argument in table_query."
            ) from None

        if not table_query.eq:
            raise SupabaseQueryException(
                supabase_query_exception="Invalid query parameters. Missing eq argument in table_query."
            ) from None

        return self.__fetch(**table_query.model_dump())

    def __fetch(
        self, *, table_name: str, columns: str, eq: dict
    ) -> SupabaseFetchQueryResult:
        try:
            fetch_query_result = (
                self.__database_client.table(table_name)
                .select(columns)
                .eq(**eq)
                .execute()
            )
        except APIError as exception:
            raise SupabaseQueryException(
                supabase_query_exception=exception
            ) from exception

        return SupabaseFetchQueryResult(supabase_fetch_query_result=fetch_query_result)

    def __delete(self, *, table_name: str, eq: dict) -> SupabaseDeleteQueryResult:
        try:
            delete_query_result = (
                self.__database_client.table(table_name).delete().eq(**eq).execute()
            )
        except APIError as exception:
            raise SupabaseCommandException(
                supabase_command_exception=exception
            ) from exception

        return SupabaseDeleteQueryResult(
            supabase_delete_query_result=delete_query_result
        )

    def __upsert(
        self, *, table_name: str, json: dict | tuple, constraint: str = ""
    ) -> SupabaseUpsertQueryResult:
        try:
            upsert_json: dict | list = list(json) if isinstance(json, tuple) else json

            upsert_query_result = (
                self.__database_client.table(table_name)
                .upsert(upsert_json, on_conflict=constraint)
                .execute()
            )
        except APIError as exception:
            raise SupabaseCommandException(
                supabase_command_exception=exception
            ) from exception

        return SupabaseUpsertQueryResult(
            supabase_upsert_query_result=upsert_query_result
        )


supabase_database_service = SupabaseDatabaseService()
