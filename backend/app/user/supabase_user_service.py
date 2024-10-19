from typing import cast, override
from uuid import UUID

from fastapi import HTTPException, status

from app.auth.supabase import SupabaseSignInAnonymouslyResult, SupabaseUserResult
from app.auth.supabase import supabase_auth_service as auth_service
from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.database.exceptions import DatabaseException
from app.database.supabase import supabase_database_service
from app.models import TableQuery, Token
from app.models.types import RecordKey
from app.user import User, UserService


class SupabaseUserService(UserService):
    """
    A concrete implementation of `UserService`.

    A `SupabaseUserService` uses a Supabase database service to manage the state of a `User`.
    """

    @override
    def get_user_anti_recommendations_history(
        self, user_id: UUID
    ) -> tuple[RecordKey, ...]:
        """Return a tuple containing Record keys in a User's anti-recommendation history."""

        try:
            database_service_result = supabase_database_service.query(
                TableQuery(
                    table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                    columns="anti_recommendations_history",
                    eq={"column": "user_id", "value": str(user_id)},
                )
            )
        except DatabaseException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to get anti-recommendation history of User with id: {user_id!s} from database. Encountered database exception: {exception.message}",
            ) from exception

        if not database_service_result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to get anti-recommendation history of User with id {user_id!s} from database. Check Supabase fetch query parameters",
            ) from None

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
    def add_to_user_anti_recommendations_history(
        self, *, user_id: UUID, anti_recommendation_key: RecordKey
    ) -> None:
        """Append `anti_recommendation_key` to a User's anti-recommendation history."""

        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )

            anti_recommendations_history.append(anti_recommendation_key)

            database_service_result = supabase_database_service.command(
                TableQuery(
                    table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                    upsert_json={
                        "anti_recommendations_history": anti_recommendations_history,
                    },
                    constraint=str(user_id),
                )
            )

        except DatabaseException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to add anti-recommendation to history of User with id {user_id!s} into database. Encountered database exception: {exception.message}",
            ) from exception

        if not database_service_result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to add anti-recommendation to history of User with id {user_id!s} into database. Check Supabase upsert query parameters.",
            ) from None

    @override
    def remove_slice_from_user_anti_recommendations_history(
        self, *, user_id: UUID, start_index: int, end_index: int
    ) -> None:
        """
        Remove a slice of anti-recommendations from a User's anti-recommendation history.

        The slice is within the range [`start_index`,`end_index`-1].
        """
        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )

            del anti_recommendations_history[start_index:end_index]

            database_service_result = supabase_database_service.command(
                TableQuery(
                    table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                    upsert_json={
                        "anti_recommendations_history": anti_recommendations_history,
                    },
                    constraint=str(user_id),
                )
            )

        except DatabaseException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to remove anti-recommendation from history of User with id {user_id!s} in database. Encountered database exception: {exception.message}",
            ) from exception

        if not database_service_result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to remove anti-recommendation from history of User with id {user_id!s} in database. Check Supabase upsert query parameters.",
            ) from None

    def create_user_from_id(self, user_id: UUID) -> User:
        """Return a new User, with an id matching `user_id`."""

        return User(id=user_id, _service=self)

    def create_user_from_token(self, token: Token) -> User:
        """
        Return a new `User` with an id that corresponds to an authentication `token`.

        If no such User is found, return a new User with an anonymous id.
        """

        user_result = cast(SupabaseUserResult, auth_service.get_user(token))

        if not user_result.succeeded:
            user_id = cast(
                SupabaseSignInAnonymouslyResult, auth_service.sign_in_anonymously()
            ).user.id
        else:
            user_id = user_result.user_id

        return self.create_user_from_id(user_id)
