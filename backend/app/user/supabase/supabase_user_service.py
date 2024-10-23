from typing import cast, override
from uuid import UUID

import supabase
from postgrest import APIError, APIResponse
from supabase import Client

from app.auth import AuthService
from app.auth.supabase import SupabaseAuthException, SupabaseAuthResponse
from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.models import AntiRecommendationsSelector, AuthToken, Settings
from app.models.types import RecordKey
from app.user import User, UserService
from app.user.supabase import SupabaseUserServiceException


class SupabaseUserService(UserService):
    """
    A concrete implementation of `UserService`.

    A `SupabaseUserService` uses a Supabase database service to manage the state of a `User`.
    """

    def __init__(self, auth_service: AuthService, settings: Settings) -> None:
        self.__auth_service = auth_service
        self.__database_client: Client = supabase.create_client(
            settings.supabase_url, settings.supabase_key
        )

    def __fetch(self, *, table_name: str, columns: str, eq: dict) -> APIResponse:

        return (
            self.__database_client.table(table_name).select(columns).eq(**eq).execute()
        )

    def __upsert(
        self, *, table_name: str, json: dict | tuple, constraint: str = ""
    ) -> APIResponse:

        upsert_json: dict | list = list(json) if isinstance(json, tuple) else json

        return (
            self.__database_client.table(table_name)
            .upsert(upsert_json, on_conflict=constraint)
            .execute()
        )

    @override
    def add_to_user_anti_recommendations_history(
        self, *, user_id: UUID, anti_recommendation_key: RecordKey
    ) -> None:
        """Append `anti_recommendation_key` to a User's anti-recommendation history."""

        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )

            anti_recommendations_history.append(anti_recommendation_key)

            self.__upsert(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                json={
                    "anti_recommendations_history": anti_recommendations_history,
                },
                constraint=str(user_id),
            )
        except APIError as exception:
            raise SupabaseUserServiceException(
                message=f"Unable to add anti-recommendation to history of User with id {user_id} into database. Encountered database exception: {exception.message}"
            ) from exception

    @override
    def get_user_anti_recommendations_history(
        self, user_id: UUID
    ) -> tuple[RecordKey, ...]:
        """Return a tuple containing Record keys in a User's anti-recommendation history."""

        try:
            database_service_result = self.__fetch(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                columns="anti_recommendations_history",
                eq={"column": "user_id", "value": str(user_id)},
            )
        except APIError as exception:
            raise SupabaseUserServiceException(
                message=f"Unable to get anti-recommendation history of User with id: {user_id} from database. Encountered database exception: {exception.message}"
            ) from exception

        return tuple(database_service_result.data[0]["anti_recommendations_history"])

    @override
    def get_user_last_seen_anti_recommendation(self, user_id: UUID) -> str:
        """Return the last Record key in a User's anti-recommendation history."""

        anti_recommendations_history = self.get_user_anti_recommendations_history(
            user_id
        )

        if anti_recommendations_history:
            return anti_recommendations_history[-1]

        return ""

    @override
    def remove_slice_from_user_anti_recommendations_history(
        self,
        *,
        user_id: UUID,
        anti_recommendations_slice: AntiRecommendationsSelector.Slice,
    ) -> None:
        """
        Remove a slice of anti-recommendations from a User's anti-recommendation history.

        """
        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )[
                anti_recommendations_slice.start_index : anti_recommendations_slice.end_index
            ]

            self.__upsert(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                json={
                    "anti_recommendations_history": anti_recommendations_history,
                },
                constraint=str(user_id),
            )

        except APIError as exception:
            raise SupabaseUserServiceException(
                message=f"Unable to remove anti-recommendation from history of User with id {user_id} in database. Encountered database exception: {exception.message}"
            ) from exception

    def create_user_from_id(self, user_id: UUID) -> User:
        """Return a new User, with an id matching `user_id`."""

        return User(id=user_id, _service=self)

    def create_user_from_token(self, token: AuthToken) -> User:
        """
        Return a new `User` with an id that corresponds to an authentication `token`.

        If no such User is found, return a new User with an anonymous id.
        """

        try:
            user_result = cast(
                SupabaseAuthResponse, self.__auth_service.get_user(token)
            )
        except SupabaseAuthException:
            try:
                user_result = cast(
                    SupabaseAuthResponse,
                    self.__auth_service.sign_in_anonymously(),
                )
            except SupabaseAuthException as exception:
                raise SupabaseUserServiceException(
                    message=f"Unable to get anonymous User ID. Encountered authentication exception with the message: {exception.message}"
                ) from exception

        return self.create_user_from_id(user_result.user_id)
