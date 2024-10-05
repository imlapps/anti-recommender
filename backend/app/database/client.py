from typing import cast

from postgrest import APIResponse, SyncFilterRequestBuilder, SyncSelectRequestBuilder
from supabase import Client, create_client

from app.models import settings


class DatabaseClient:
    """A Database client class."""

    def __init__(self) -> None:
        self.__database_client: Client | None = self.__select_database_client()

    def delete(self, *, table_name: str, eq: dict) -> APIResponse | None:
        if self.__database_client:
            return cast(
                SyncFilterRequestBuilder,
                self.__database_client.table(table_name).delete().eq(**eq),
            ).execute()
        return None

    def fetch(self, *, table_name: str, query: str, eq: dict) -> APIResponse | None:
        if self.__database_client:
            return cast(
                SyncSelectRequestBuilder,
                self.__database_client.table(table_name).select(query).eq(**eq),
            ).execute()
        return None

    def insert(self, *, table_name: str, query: dict | list) -> APIResponse | None:
        if self.__database_client:
            return self.__database_client.table(table_name).insert(query).execute()
        return None

    def __select_database_client(self) -> Client | None:
        if settings.supabase_url and settings.supabase_key:
            return create_client(settings.supabase_url, settings.supabase_key)

        return None

    def update(self, *, table_name: str, query: dict, eq: dict) -> APIResponse | None:
        if self.__database_client:
            return cast(
                SyncFilterRequestBuilder,
                self.__database_client.table(table_name).update(query).eq(**eq),
            ).execute()
        return None

    def upsert(
        self, table_name: str, query: dict | list, constraint: str = ""
    ) -> APIResponse | None:
        if self.__database_client:
            return (
                self.__database_client.table(table_name)
                .upsert(query, on_conflict=constraint)
                .execute()
            )
        return None


database_client = DatabaseClient()
