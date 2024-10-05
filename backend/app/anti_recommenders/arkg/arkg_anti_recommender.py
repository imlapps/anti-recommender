from typing import override
from collections.abc import Iterable
from pathlib import Path

import pyoxigraph as ox

from app.anti_recommenders import AntiRecommender
from app.constants import (
    WIKIPEDIA_BASE_URL,
    ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
)
from app.models import (
    AntiRecommendation,
    User,
    UserState,
)
from app.models.types import RdfMimeType, RecordKey, StoreQuery
from app.namespaces import SCHEMA
from app.database import databaseClient
from postgrest import APIResponse, APIError
import logging


class ArkgAntiRecommender(AntiRecommender):
    """
    A concrete implementation of `AntiRecommender`.

    `ArkgAntiRecommender` uses information stored in an Anti-Recommendation Knowledge Graph to generate `AntiRecommendations`.
    """

    def __init__(
        self,
        *,
        base_iri: ox.NamedNode,
        file_path: Path,
        mime_type: RdfMimeType,
        record_keys: tuple[RecordKey, ...],
        user: User,
    ) -> None:
        self.__base_iri = base_iri
        self.__logger = logging.getLogger(__name__)
        self.__record_keys: tuple[RecordKey, ...] = record_keys
        self.__store: ox.Store = self.__load_store(
            file_path=file_path, mime_type=mime_type, base_iri=base_iri
        )
        self.__user_state: UserState = self.__fetch_user_state_from_database(user)
        

    def __fetch_anti_recommendations_query(self, record_key: RecordKey) -> StoreQuery:
        """
        Return a `SPARQL` query that fetches anti-recommendations of `record_key` from an `ARKG Store`.
        """

        return f"SELECT ?title WHERE {{ <{record_key}> <{SCHEMA.ITEM_REVIEWED.value}> ?resource {{?resource <{SCHEMA.TITLE.value}> ?title}} }}"
    
    def __fetch_user_state_from_database(self, user: User) -> UserState:
        """
        Fetch and return the state of a `User` from a database.

        Return a new `UserState` if none is present in the database.
        """
        try:
            api_response = databaseClient.fetch(
                table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
                query="*",
                eq={"column": "user_id", "value": user.id},
            )
        except APIError as exception:
            self.__logger.warning(
                f"Error fetching user state from database.\
                    Error message: {exception.json().get("message")}"
            )
            return

        if api_response.data:
            return UserState(**api_response.data[0])

        return UserState(user_id=user.id, anti_recommendations_history={})

    @staticmethod
    def __load_store(
        base_iri: ox.NamedNode, file_path: Path, mime_type: RdfMimeType
    ) -> ox.Store:
        """Load an `ARKG` serialization into an `RDF Store`."""

        return ox.Store.load(
            input=file_path,
            mime_type=mime_type.value,
            base_iri=base_iri.value,
        )
    
    def __retrieve_anti_recommendations_from_store(
        self, record_key: RecordKey
    ) -> tuple[AntiRecommendation, ...]:
        """Return a tuple of `AntiRecommendations` that have been retrieved from an `ARKG Store`."""

        return tuple(
            binding["title"].value
            for binding in self.__store.query(  # type: ignore[union-attr]
                query=self.__fetch_anti_recommendations_query(record_key),
                base_iri=self.__base_iri.value,
            )
        )
    
    def __upsert_user_state_into_database(self) -> None:
        """Upsert a `UserState` into a database."""

        try:
            databaseClient.upsert(
            table_name=ARKG_ANTI_RECOMMENDER_USER_STATE_TABLE_NAME,
            query=self.__user_state.model_dump(
                by_alias=True, exclude={"created_at", "last_updated"}
            ),
            constraint=self.__user_state.id,
        )
        except APIError as exception:
            self.__logger.warning(
                f"Error upserting user state into database.\
                    Error message: {exception.json().get("message")}"
            )
            return
    
    @override
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """
        Generate anti-recommendations of a Record.

        Anti-recommendations are obtained from an ARKG.
        """

        anti_recommendations = [
            unseen_anti_recommendation_key
            for unseen_anti_recommendation_key in self.__retrieve_anti_recommendations_from_store(
                record_key
            )
            if unseen_anti_recommendation_key
            not in self.__user_state.anti_recommendations_history.values()
        ]

        if not anti_recommendations:
            anti_recommendations = [
                unseen_anti_recommendation_key
                for unseen_anti_recommendation_key in self.__record_keys
                if unseen_anti_recommendation_key
                not in self.__user_state.anti_recommendations_history.values()
            ]

        anti_recommendation_key = anti_recommendations[0]
        self.__user_state.anti_recommendations_history.update(
            {"anti_recommendation_key": anti_recommendation_key}
        )

        self.__upsert_user_state_into_database()

        return tuple(
            AntiRecommendation(
                key=anti_recommendation_key,
                url=WIKIPEDIA_BASE_URL + anti_recommendation_key,
            )
        )
