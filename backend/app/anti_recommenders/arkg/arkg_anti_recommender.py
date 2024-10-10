import logging
from collections.abc import Iterable
from pathlib import Path
from typing import override

import pyoxigraph as ox
from postgrest import APIError

from app.anti_recommenders import AntiRecommender
from app.constants import WIKIPEDIA_BASE_URL
from app.models import AntiRecommendation, UserState
from app.models.types import RdfMimeType, RecordKey, StoreQuery
from app.namespaces import SCHEMA
from app.utils import upsert_user_state_into_database


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
        user_state: UserState,
    ) -> None:
        self.__base_iri = base_iri
        self.__logger = logging.getLogger(__name__)
        self.__record_keys: tuple[RecordKey, ...] = record_keys
        self.__store: ox.Store = self.__load_store(
            file_path=file_path, mime_type=mime_type, base_iri=base_iri
        )
        self.__user_state = user_state

    def __fetch_anti_recommendations_query(self, record_key: RecordKey) -> StoreQuery:
        """
        Return a `SPARQL` query that fetches anti-recommendations of `record_key` from an `ARKG Store`.
        """

        return f"SELECT ?title WHERE {{ <{record_key}> <{SCHEMA.ITEM_REVIEWED.value}> ?resource {{?resource <{SCHEMA.TITLE.value}> ?title}} }}"

    @staticmethod
    def __load_store(
        base_iri: ox.NamedNode, file_path: Path, mime_type: RdfMimeType
    ) -> ox.Store:
        """Load an `ARKG` serialization into an `RDF Store`."""

        store = ox.Store()
        store.load(
            input=file_path,
            mime_type=mime_type.value,
            base_iri=base_iri.value,
        )
        return store

    def __retrieve_anti_recommendations_from_store(
        self, record_key: RecordKey
    ) -> tuple[RecordKey, ...]:
        """Return a tuple of `AntiRecommendations` that have been retrieved from an `ARKG Store`."""

        return tuple(
            binding["title"].value
            for binding in self.__store.query(  # type: ignore[union-attr]
                query=self.__fetch_anti_recommendations_query(record_key),
                base_iri=self.__base_iri.value,
            )
        )

    def __select_primary_anti_recommendation_key(
        self, anti_recommendation_keys: tuple[RecordKey, ...]
    ) -> RecordKey | None:
        """
        Select and return a primary anti-recommendation key.

        A primary anti-recommendation key is a `Recordkey` that has not yet been visited by a `User`.

        A primary anti-recommendation key is first looked for in `anti_recommendation_keys`

        If no unseen key is found in anti_recommendation_keys, the first unseen key in `__record_keys` is returned.
        """

        if self.__user_state:
            primary_anti_recommendation_keys = [
                unseen_anti_recommendation_key
                for unseen_anti_recommendation_key in anti_recommendation_keys
                if unseen_anti_recommendation_key
                not in self.__user_state.anti_recommendations_history.values()
            ]

            if not primary_anti_recommendation_keys:
                primary_anti_recommendation_keys = [
                    unseen_anti_recommendation_key
                    for unseen_anti_recommendation_key in self.__record_keys
                    if unseen_anti_recommendation_key
                    not in self.__user_state.anti_recommendations_history.values()
                ]

            if primary_anti_recommendation_keys:
                return primary_anti_recommendation_keys[0]

        return None

    @override
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """
        Generate anti-recommendations of a `Record`.

        Anti-recommendations are obtained from an `ARKG`.

        The first anti-recommendation generated is an anti-recommendation that has not yet been seen by a `User`.

        All other anti-recommendations may or may not have been seen by a User.
        """

        if self.__user_state:
            anti_recommendation_keys = list(
                self.__retrieve_anti_recommendations_from_store(record_key)
            )

            primary_anti_recommendation_key = (
                self.__select_primary_anti_recommendation_key(
                    tuple(anti_recommendation_keys)
                )
            )

            if primary_anti_recommendation_key:
                if primary_anti_recommendation_key in anti_recommendation_keys:
                    anti_recommendation_keys.remove(primary_anti_recommendation_key)

                anti_recommendation_keys.insert(0, primary_anti_recommendation_key)

                self.__user_state.anti_recommendations_history.update(
                    {"anti_recommendation_key": primary_anti_recommendation_key}
                )

                try:
                    upsert_user_state_into_database(self.__user_state)

                    return (
                        AntiRecommendation(
                            key=anti_recommendation_key,
                            url=WIKIPEDIA_BASE_URL + anti_recommendation_key,
                        )
                        for anti_recommendation_key in anti_recommendation_keys
                    )
                except APIError as exception:
                    self.__logger.warning(
                        f"Could not generate valid anti-recommendations because of error in ArkgAntiRecommender.__upsert_user_state_into_database.\
                        Error message: {exception.json().get("message")}"
                    )

        return ()
