from fastapi import HTTPException, status
from postgrest import APIError

from app.constants import ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME
from app.database import database_client
from app.models import UserState


def upsert_user_state_into_database(user_state: UserState) -> None:
    """Upsert a `UserState` into a database."""

    if user_state:
        try:
            database_client.upsert(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                query=user_state.model_dump(by_alias=True),
                constraint=str(user_state.id),
            )
        except APIError as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to upsert UserState into database. Encountered APIError with exception: {exception}",
            ) from exception
