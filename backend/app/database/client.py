from typing import cast

import supabase
from postgrest import APIResponse, SyncFilterRequestBuilder, SyncSelectRequestBuilder
from supabase import Client

from app.models import settings


class DatabaseClient:
    """A database client class."""

    def __init__(self) -> None:
        self.__database_client: Client | None = self.__select_database_client()

    def __select_database_client(self) -> Client | None:
        """
        Create and return a database client.

        A Supabase `Client` instance is returned if the required parameters are in `settings`.
        """

        if settings.supabase_url and settings.supabase_key:
            return supabase.create_client(settings.supabase_url, settings.supabase_key)

        return None

    def delete(self, *, table_name: str, eq: dict) -> APIResponse | None:
        """
        Run a `DELETE` query on a table with the name `table_name`.

        An `equal_to` filter is added to the query via the `eq` parameter.
        """

        if isinstance(self.__database_client, Client):
            return cast(
                SyncFilterRequestBuilder,
                self.__database_client.table(table_name).delete().eq(**eq),
            ).execute()
        return None

    def fetch(self, *, table_name: str, query: str, eq: dict) -> APIResponse | None:
        """
        Run a `SELECT` query on a table with the name `table_name`.

        An `equal_to` filter is added to the query via the `eq` parameter.
        """

        if isinstance(self.__database_client, Client):
            return cast(
                SyncSelectRequestBuilder,
                self.__database_client.table(table_name).select(query).eq(**eq),
            ).execute()
        return None

    def insert(self, *, table_name: str, query: dict | list) -> APIResponse | None:
        """Run a `INSERT` query on a table with the name `table_name`."""

        if isinstance(self.__database_client, Client):
            return self.__database_client.table(table_name).insert(query).execute()
        return None

    def update(self, *, table_name: str, query: dict, eq: dict) -> APIResponse | None:
        """
        Run an `UPDATE` query on a table with the name `table_name`.

        An `equal_to` filter is added to the query via the `eq` parameter.
        """

        if isinstance(self.__database_client, Client):
            return cast(
                SyncFilterRequestBuilder,
                self.__database_client.table(table_name).update(query).eq(**eq),
            ).execute()
        return None

    def upsert(
        self, table_name: str, query: dict | list, constraint: str = ""
    ) -> APIResponse | None:
        """
        Run an `UPSERT` query on a table with the name `table_name`.

        An `UPDATE` query is run if there is a column conflict with `constraint`.

        An `INSERT` query is run otherwise.
        """

        if isinstance(self.__database_client, Client):
            return (
                self.__database_client.table(table_name)
                .upsert(query, on_conflict=constraint)
                .execute()
            )
        return None


database_client = DatabaseClient()
