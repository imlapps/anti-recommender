from app.anti_recommenders import AntiRecommender
from app.anti_recommenders.arkg.arkg_anti_recommender import ArkgAntiRecommender
from app.anti_recommenders.openai import NormalOpenaiAntiRecommender
from app.models import Record, UserState, settings
from app.models.types import AntiRecommenderType, RecordKey
from app.readers import AllSourceReader


class AntiRecommendationEngine:
    """
    AntiRecommendationEngine for the NerdSwipe backend.

    An AntiRecommendationEngine reaches out to an AntiRecommender to retrieve AntiRecommendations of a record_key.

    An AntiRecommendationEngine consists of:
        - __records_by_key: A dictionary of type RecordKey: Record, that holds Records obtained from storage.
        - __current_anti_recommendation_records: A list of Records that are currently used for anti-recommendations.
        - __stack: A stack that stores a list of Records that were previously used for anti-recommendations.

    An AntiRecommendationEngine also:
        - Returns a tuple of Records that match the AntiRecommendations of the first key in __records_by_key.
        - Returns a tuple of Records that match the AntiRecommendations of a record_key.
        - Returns a tuple of Records that matched the previous AntiRecommendations.
    """

    def __init__(self) -> None:
        self.__anti_recommender: AntiRecommender | None = None
        self.__current_anti_recommendation_records: list[Record] = []
        self.__records_by_key: dict[RecordKey, Record] = {
            record.key: record for record in AllSourceReader().read()
        }
        self.__stack: list[list[Record]] = []

    @staticmethod
    def select_anti_recommender(
        *, user_state: UserState, record_keys: tuple[Record, ...]
    ) -> AntiRecommender | None:
        """Select and return an `AntiRecommender` based on values stored in `settings`."""

        if (
            settings.anti_recommender_type == AntiRecommenderType.OPEN_AI
            and settings.openai_api_key
        ):
            return NormalOpenaiAntiRecommender()

        if settings.anti_recommender_type == AntiRecommenderType.ARKG:
            record_keys_list = list(record_keys)
            record_keys_list.sort()

            return ArkgAntiRecommender(
                base_iri=settings.arkg_base_iri,
                file_path=settings.arkg_file_path,
                mime_type=settings.arkg_mime_type,
                record_keys=tuple(record_keys_list),
                user_state=user_state,
            )

        return None

    def initialize_anti_recommender(self, user_state: UserState) -> None:
        """Initialize an anti-recommender in the `AntiRecommendationEngine`."""

        self.__anti_recommender = self.select_anti_recommender(
            user_state=user_state, record_keys=self.__records_by_key.keys()
        )

    def initial_records(
        self, *, record_key: RecordKey | None = None
    ) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same key as AntiRecommendations of the first key in __records_by_key."""

        if record_key:
            return self.next_records(record_key=record_key)

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

        return tuple(records_of_anti_recommendations)

    def previous_records(self) -> tuple[Record, ...]:
        """
        Return a tuple of Records that matched the previous AntiRecommendations.

        Return an empty tuple if there were no such Records.
        """

        if self.__stack:
            return tuple(self.__stack.pop())

        return ()
