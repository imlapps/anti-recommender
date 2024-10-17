from uuid import UUID

from fastapi import HTTPException, status

from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.database import DatabaseException
from app.database.supabase import supabase_database_service as database_service
from app.models import TableQuery, User, UserState


def fetch_user_state_from_database(user: User) -> UserState:
    """
    Fetch and return the state of a `User` from a database.

    Return a new `UserState` if none is present in the database.
    """

    try:
        database_service_result = database_service.query(
            TableQuery(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                columns="*",
                eq={"column": "user_id", "value": str(user.id)},
            )
        )
    except DatabaseException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch UserState from database. Encountered DatabaseException: {exception}",
        ) from exception

    if database_service_result.succeeded:
        response = database_service_result.data[0]
        return UserState(
            user_id=UUID(str(response["user_id"])),
            anti_recommendations_history=response["anti_recommendations_history"],
        )

    return UserState(user_id=user.id, anti_recommendations_history={})
