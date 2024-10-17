from fastapi import HTTPException, status

from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.database import DatabaseException
from app.database.supabase import supabase_database_service as database_service
from app.models import TableQuery, UserState


def upsert_user_state_into_database(user_state: UserState) -> None:
    """Upsert a `UserState` into a database."""

    if user_state:
        try:
            database_service_result = database_service.command(
                TableQuery(
                    table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                    upsert_json=user_state.model_dump(by_alias=True),
                    constraint=str(user_state.id),
                )
            )

            if not database_service_result.succeeded:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unable to upsert UserState into database. Check Upsert query parameters.",
                ) from None

        except DatabaseException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to upsert UserState into database. Encountered database exception: {exception}",
            ) from exception
