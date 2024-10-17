from uuid import UUID
from typing import override
from fastapi import HTTPException, status
from app.user import UserService, User
from app.database.supabase import supabase_database_service
from app.models import TableQuery
from app.models.types import RecordKey
from app.database.exceptions import DatabaseException
from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME


class SupabaseUserService(UserService):
    @override
    def delete_user(self, user_id: UUID):
        try:
            database_command_result = supabase_database_service.command(
                TableQuery(
                    table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                    eq={"column": "user_id", "value": str(user_id)},
                )
            )

        except DatabaseException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to delete user from database. Encountered database exception: {exception}",
            ) from exception

        if not database_command_result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to delete user from database. Check database query parameters.",
            ) from None

    @override
    def get_user_anti_recommendations_history(
        self, user_id: UUID
    ) -> tuple[RecordKey, ...]:
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
                detail=f"Unable to fetch anti_recommendations_history from database. Encountered database exception: {exception}",
            ) from exception

        if not database_service_result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to fetch anti_recommendations_history from database. Check database query parameters",
            ) from None

        return tuple(database_service_result.data[0]["anti_recommendations_history"])

    @override
    def get_user_last_seen_anti_recommendation(self, user_id: UUID) -> str:
        anti_recommendations_history = self.get_user_anti_recommendations_history(
            user_id
        )

        if anti_recommendations_history:
            return anti_recommendations_history[-1]

        return ""

    @override
    def update_user_anti_recommendations_history(
        self, *, user_id: UUID, anti_recommendation_key: RecordKey
    ) -> None:
        try:
            anti_recommendations_history = list(
                self.get_user_anti_recommendations_history(user_id)
            )

            anti_recommendations_history.append(anti_recommendation_key)

            database_service_result = supabase_database_service.command(
                TableQuery(
                    table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                    upsert_json={
                        "last_seen_anti_recommendation": anti_recommendation_key,
                        "anti_recommendations_history": anti_recommendations_history,
                    },
                    constraint=str(user_id),
                )
            )

        except DatabaseException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to upsert anti-recommendation into database. Encountered database exception: {exception}",
            ) from exception

        if not database_service_result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to upsert anti-recommendation into database. Check upsert query parameters.",
            ) from None

    def get_user(self, user_id: UUID) -> User:

        return User(id=user_id, _service=self)
