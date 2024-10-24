from app.anti_recommenders import AntiRecommender
from app.anti_recommenders.arkg.arkg_anti_recommender import ArkgAntiRecommender
from app.anti_recommenders.openai import NormalOpenaiAntiRecommender
from app.models import Record, Settings
from app.models.anti_recommendations_selector import AntiRecommendationsSelector
from app.models.types import AntiRecommenderType, RecordKey
from app.readers import AllSourceReader
from app.user import User


class AntiRecommendationEngine:
    """
    AntiRecommendationEngine for the NerdSwipe backend.

    An AntiRecommendationEngine reaches out to an AntiRecommender to retrieve AntiRecommendations of a record_key.

    An AntiRecommendationEngine consists of:
        - __anti_recommender: An AntiRecommnder for the AntiRecommedationEngine.
        - __current_anti_recommendation_records: A list of Records that are currently used for anti-recommendations.
        - __records_by_key: A dictionary of type RecordKey: Record, that holds Records obtained from storage.
        - __stack: A stack that stores a list of Records that were previously used for anti-recommendations.
        - __user: The User of the current session.

    An AntiRecommendationEngine also:
        - Returns a tuple of Records that match the AntiRecommendations of the first key in __records_by_key.
        - Returns a tuple of Records that match the AntiRecommendations of a record_key.
        - Returns a tuple of Records that matched the previous AntiRecommendations.
        - Resets itself by clearing all variables related to a previous session and set __user to a new object.
    """

    def __init__(self, user: User, settings: Settings) -> None:
        self.__anti_recommender: AntiRecommender = self.__select_anti_recommender(
            settings
        )
        self.__current_anti_recommendation_records: list[Record] = []
        self.__records_by_key: dict[RecordKey, Record] = {
            record.key: record for record in AllSourceReader().read()
        }
        self.__stack: list[list[Record]] = []
        self.__user = user

    def __select_anti_recommender(self, settings: Settings) -> AntiRecommender:
        """
        Select and return an `AntiRecommender` based on values stored in `settings`.

        An `ArkgAntiRecommender` is the default AntiRecommender selection.
        """

        if (
            settings.anti_recommender_type == AntiRecommenderType.OPEN_AI
            and settings.openai_api_key
        ):
            return NormalOpenaiAntiRecommender()

        return ArkgAntiRecommender(
            base_iri=settings.arkg_base_iri,
            file_path=settings.arkg_file_path,
            mime_type=settings.arkg_mime_type,
            record_keys=tuple(sorted(self.__records_by_key.keys())),
            user=self.__user,
        )

    def initial_records(self) -> tuple[Record, ...]:
        """Return an initial tuple of Records."""

        last_seen_anti_recommendation_key = (
            self.__user.last_seen_anti_recommendation_key
        )

        if last_seen_anti_recommendation_key:
            return self.next_records(record_key=last_seen_anti_recommendation_key)

        return self.next_records(record_key=next(iter(self.__records_by_key.keys())))

    def next_records(self, *, record_key: RecordKey) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same key as the AntiRecommendations of record_key."""

        records_of_anti_recommendations: list[Record] = []

        if self.__anti_recommender:
            # Retrieve Records that have the same key as the generated AntiRecommendations.
            records_of_anti_recommendations = [
                self.__records_by_key[anti_recommendation.key]
                for anti_recommendation in self.__anti_recommender.generate_anti_recommendations(
                    record_key=record_key
                )
                if anti_recommendation.key in self.__records_by_key
            ]

        if records_of_anti_recommendations:
            if self.__current_anti_recommendation_records:
                self.__stack.append(self.__current_anti_recommendation_records)

            self.__current_anti_recommendation_records = [
                self.__records_by_key[record_key],
                *records_of_anti_recommendations,
            ]

            self.__user.add_anti_recommendation_to_history(
                records_of_anti_recommendations[0].key
            )

        return tuple(records_of_anti_recommendations)

    def previous_records(self) -> tuple[Record, ...]:
        """
        Return a tuple of Records that matched the previous AntiRecommendations.

        If __anti_recommender is an ArkgAntiRecommender instance, the last 2 anti-recommendations are removed from __user's history.

        Return an empty tuple if there were no such Records.
        """

        if self.__stack:
            self.__user.remove_anti_recommendations_slice_from_history(
                AntiRecommendationsSelector.SELECT_ALL_BUT_LAST_TWO_RECORDS
            )

            return tuple(self.__stack.pop())

        return ()
