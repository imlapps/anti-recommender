from fastapi import HTTPException, status
from postgrest import APIError

from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.database import database_client
from app.models.user import User
from app.models.user_state import UserState


def fetch_user_state_from_database(user: User) -> UserState:
    """
    Fetch and return the state of a `User` from a database.

    Return a new `UserState` if none is present in the database.
    """

    try:
        api_response = database_client.fetch(
            table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
            query="*",
            eq={"column": "user_id", "value": str(user.id)},
        )
    except APIError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch UserState from database. Encountered APIError with exception: {exception}",
        ) from exception

    if api_response and api_response.data:
        return UserState(**api_response.data[0])

    return UserState(user_id=user.id, anti_recommendations_history={})
