from typing import cast

from postgrest import APIResponse, SyncFilterRequestBuilder, SyncSelectRequestBuilder
from supabase import Client, create_client

from app.models import settings


class DatabaseClient:
    """A Database client class."""

    def __init__(self) -> None:
        self.__database_client: Client = self.__select_database_client()

    def delete(self, *, table_name: str, eq: str) -> None:
        return cast(
            SyncFilterRequestBuilder,
            self.__database_client.table(table_name).delete().eq(str(eq)),
        ).execute()

    def fetch(self, *, table_name: str, query: str, eq: str | None) -> APIResponse:
        return cast(
            SyncSelectRequestBuilder,
            self.__database_client.table(table_name).select(query).eq(str(eq)),
        ).execute()

    def insert(self, *, table_name: str, query: dict | list) -> APIResponse:
        return self.__database_client.table(table_name).insert(query).execute()

    def __select_database_client(self) -> Client | None:
        if settings.supabase_url and settings.supabase_key:
            return create_client(settings.supabase_url, settings.supabase_key)

        return None

    def update(self, *, table_name: str, query: dict, eq: str | None) -> APIResponse:
        return cast(
            SyncFilterRequestBuilder,
            self.__database_client.table(table_name).update(query).eq(str(eq)),
        ).execute()

    def upsert(self, table_name: str, query: str, constraint: str = "") -> None:
        return cast(
            self.__database_client.table(table_name).upsert(
                query, on_conflict=constraint
            )
        )
