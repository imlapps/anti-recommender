from collections.abc import Iterable
from pathlib import Path
from typing import override

import pyoxigraph as ox
from pydantic import AnyUrl
from pydantic_extra_types.language_code import LanguageAlpha2

from app.anti_recommenders import AntiRecommender
from app.constants import WIKIPEDIA_BASE_URL
from app.models import AntiRecommendation
from app.models.types import RdfMimeType, RecordKey
from app.namespaces import SCHEMA
from app.user import User


class ArkgAntiRecommender(AntiRecommender):
    """
    A concrete implementation of AntiRecommender.

    An ArkgAntiRecommender uses information stored in an Anti-Recommendation Knowledge Graph to generate anti-recommendations.
    """

    def __init__(
        self,
        *,
        file_path: Path,
        mime_type: RdfMimeType,
        record_keys: tuple[RecordKey, ...],
        user: User,
    ) -> None:
        self.__record_keys: tuple[RecordKey, ...] = record_keys
        self.__store: ox.Store = self.__load_store(
            file_path=file_path, mime_type=mime_type
        )
        self.__user = user

    @staticmethod
    def __load_store(*, file_path: Path, mime_type: RdfMimeType) -> ox.Store:
        """Load an ARKG serialization into an RDF Store."""

        store = ox.Store()
        store.load(
            input=file_path,
            mime_type=mime_type.value,
        )
        return store

    def __retrieve_anti_recommendations_from_store(
        self, *, record_key: RecordKey, language: LanguageAlpha2
    ) -> tuple[RecordKey, ...]:
        """Return a tuple of anti-recommendations that have been retrieved from an ARKG Store."""

        return tuple(
            binding["name"].value
            for binding in self.__store.query(  # type: ignore[union-attr]
                query=f'SELECT ?name WHERE {{ {{ ?uuid <{SCHEMA.ABOUT.value}> ?entity {{ ?entity_article <{SCHEMA.ABOUT.value}> ?entity {{?entity_article <{SCHEMA.NAME.value}> "{record_key}"@{language} }} }} . \
                                                 ?uuid <{SCHEMA.ITEM_REVIEWED.value}> ?anti_recommendation {{?anti_recommendation_article <{SCHEMA.ABOUT.value}> ?anti_recommendation {{?anti_recommendation_article <{SCHEMA.NAME.value}> ?name}} }} }} }}'
            )
        )

    def __select_primary_anti_recommendation_key(
        self, *, anti_recommendation_keys: tuple[RecordKey, ...]
    ) -> RecordKey:
        """
        Select and return a primary anti-recommendation key.

        A primary anti-recommendation key is a Recordkey that has not yet been visited by a User.

        A primary anti-recommendation key is first looked for in anti_recommendation_keys.

        If no unseen key is found in anti_recommendation_keys, the first unseen key in __record_keys is returned.
        """

        anti_recommendations_history = list(self.__user.anti_recommendations_history)
        primary_anti_recommendation_keys = [
            unseen_anti_recommendation_key
            for unseen_anti_recommendation_key in anti_recommendation_keys
            if unseen_anti_recommendation_key not in anti_recommendations_history
        ]

        if not primary_anti_recommendation_keys:
            primary_anti_recommendation_keys = [
                unseen_anti_recommendation_key
                for unseen_anti_recommendation_key in self.__record_keys
                if unseen_anti_recommendation_key not in anti_recommendations_history
            ]

        return primary_anti_recommendation_keys[0]

    @override
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """
        Generate AntiRecommendations of a record_key.

        Anti-recommendations are obtained from an ARKG.

        The first anti-recommendation generated is an anti-recommendation that has not yet been seen by a User.

        All other anti-recommendations may or may not have been seen by a User.
        """

        anti_recommendation_keys = list(
            self.__retrieve_anti_recommendations_from_store(
                record_key=record_key, language=LanguageAlpha2("en")
            )
        )

        primary_anti_recommendation_key = self.__select_primary_anti_recommendation_key(
            anti_recommendation_keys=tuple(anti_recommendation_keys)
        )

        if primary_anti_recommendation_key:
            if primary_anti_recommendation_key in anti_recommendation_keys:
                anti_recommendation_keys.remove(primary_anti_recommendation_key)

            anti_recommendation_keys.insert(0, primary_anti_recommendation_key)

            return (
                AntiRecommendation(
                    key=anti_recommendation_key,
                    url=AnyUrl(WIKIPEDIA_BASE_URL + anti_recommendation_key),
                )
                for anti_recommendation_key in anti_recommendation_keys
            )

        return ()
