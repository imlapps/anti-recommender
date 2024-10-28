from typing import override

import supabase
from postgrest import APIError, APIResponse
from supabase import Client

from app.auth import AuthException, AuthService
from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.models import AntiRecommendationsSelector, AuthToken, Settings
from app.models.types import RecordKey, UserId
from app.user import User, UserService, UserServiceException


class SupabaseUserService(UserService):
    """
    A concrete implementation of UserService.

    A SupabaseUserService uses a Supabase database to manage the state of a User.
    """

    def __init__(self, auth_service: AuthService, settings: Settings) -> None:
        self.__auth_service = auth_service
        self.__database_client: Client = self.__create_database_client(settings)

    @staticmethod
    def __create_database_client(settings: Settings) -> Client:
        """Return a Supabase database client, if Supabase URL and Supabase key are present in Settings."""

        if settings.supabase_url and settings.supabase_key:
            return supabase.create_client(
                str(settings.supabase_url), settings.supabase_key.get_secret_value()
            )

        msg = (
            "Cannot use Supabase database client without Supabase URL and Supabase key."
        )
        raise UserServiceException(msg)

    def __fetch_from_database(
        self, *, table_name: str, columns: str, eq: dict
    ) -> APIResponse:
        """
        Run a SELECT query on a table with the name table_name.

        An equal_to filter is added to the query via the eq parameter.
        """

        return (
            self.__database_client.table(table_name).select(columns).eq(**eq).execute()
        )

    def __upsert_into_database(
        self, *, table_name: str, json: dict | tuple, constraint: str = ""
    ) -> APIResponse:
        """
        Run an UPSERT query on a table with the name table_name.

        An UPDATE query is run if there is a column conflict with constraint.

        An INSERT query is run otherwise.
        """

        upsert_json: dict | list = list(json) if isinstance(json, tuple) else json

        return (
            self.__database_client.table(table_name)
            .upsert(upsert_json, on_conflict=constraint)
            .execute()
        )

    @override
    def add_to_user_anti_recommendations_history(
        self, *, user_id: UserId, anti_recommendation_key: RecordKey
    ) -> None:
        """Append anti_recommendation_key to a User's anti-recommendation history."""

        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )

            anti_recommendations_history.append(anti_recommendation_key)

            self.__upsert_into_database(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                json={
                    "anti_recommendations_history": anti_recommendations_history,
                },
                constraint=str(user_id),
            )
        except APIError as exception:
            raise UserServiceException from exception

    @override
    def get_user_anti_recommendations_history(
        self, user_id: UserId
    ) -> tuple[RecordKey, ...]:
        """Return a tuple containing Record keys in a User's anti-recommendation history."""

        try:
            database_service_result = self.__fetch_from_database(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                columns="anti_recommendations_history",
                eq={"column": "user_id", "value": str(user_id)},
            )
        except APIError as exception:
            raise UserServiceException from exception

        return tuple(database_service_result.data[0]["anti_recommendations_history"])

    @override
    def get_user_last_seen_anti_recommendation(
        self, user_id: UserId
    ) -> RecordKey | None:
        """Return the last Record key in a User's anti-recommendation history."""

        anti_recommendations_history = self.get_user_anti_recommendations_history(
            user_id
        )

        if anti_recommendations_history:
            return anti_recommendations_history[-1]

        return None

    @override
    def remove_anti_recommendations_from_user_history(
        self,
        *,
        user_id: UserId,
        selector: AntiRecommendationsSelector,
    ) -> None:
        """Use selector to remove anti-recommendations from a User's history."""

        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )
            match selector:
                case AntiRecommendationsSelector.REMOVE_LAST_TWO_RECORDS:
                    del anti_recommendations_history[-2:]
                case _:
                    raise UserServiceException from ValueError

            self.__upsert_into_database(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                json={
                    "anti_recommendations_history": anti_recommendations_history,
                },
                constraint=str(user_id),
            )

        except APIError as exception:
            raise UserServiceException from exception

    def create_user_from_id(self, user_id: UserId) -> User:
        """Return a new User, with an ID that matches user_id."""

        return User(id=user_id, _service=self)

    def __retrieve_user_id(self, authentication_token: AuthToken) -> UserId:
        """
        Return a user ID that corresponds to an authentication_token.

        If no such user ID is found, return an anonymous user ID.
        """

        try:
            user_response = self.__auth_service.get_user(authentication_token)
        except AuthException as exception:
            raise UserServiceException from exception

        if user_response.user_id:
            return user_response.user_id

        try:
            return self.__auth_service.sign_in_anonymously().user_id
        except AuthException as exception:
            raise UserServiceException from exception

    def create_user_from_token(self, authentication_token: AuthToken) -> User:
        """
        Retrieve a user ID from __auth_service, and return a new User with a matching ID.
        """

        return self.create_user_from_id(self.__retrieve_user_id(authentication_token))
