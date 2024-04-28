from app.anti_recommenders.anti_recommender import AntiRecommender
from app.anti_recommenders.open_ai.normal_open_ai_anti_recommender import (
    NormalOpenAiAntiRecommender,
)
from app.models.record import Record
from app.models.settings import settings
from app.models.types import RecordType, RecordKey
from app.readers.all_source_reader import AllSourceReader


class AntiRecommendationEngine:
    """AntiRecommendationEngine for the NerdSwipe backend.

    An AntiRecommendationEngine reaches out to an AntiRecommender to retrieve AntiRecommendations of a record_key.
    record_type is the type of AntiRecommendations retrieved from the AntiRecommender.

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
        self.__records_by_key: dict[RecordKey, Record] = {
            record.key: record for record in AllSourceReader().read()
        }
        self.__anti_recommender: AntiRecommender | None = (
            self.__select_anti_recommender()
        )
        self.__stack: list[list[Record]] = []
        self.__current_anti_recommendation_records: list[Record] = []

    def __select_anti_recommender(self) -> AntiRecommender | None:
        """Select and return an AntiRecommender based on values stored in settings."""

        if (
            settings.anti_recommender_type.lower() == "openai"
            and settings.openai_api_key
        ):
            return NormalOpenAiAntiRecommender()

        return None

    def get_initial_records(self, record_type: RecordType) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same key as AntiRecommendations of the first key in __records_by_key."""

        return self.get_next_records(
            record_key=next(iter(self.__records_by_key.keys())), record_type=record_type
        )

    def get_next_records(
        self, *, record_key: RecordKey, record_type: RecordType
    ) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same key as the AntiRecommendations of record_key."""

        records_of_anti_recommendations: list[Record] = []

        if self.__anti_recommender:

            # Retrieve Records that have the same key as the generated AntiRecommendations.
            records_of_anti_recommendations = [
                self.__records_by_key[anti_recommendation.key]
                for anti_recommendation in self.__anti_recommender.generate_anti_recommendations(
                    record_key=record_key, record_type=record_type
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

    def get_previous_records(self) -> tuple[Record, ...]:
        """Return a tuple of Records that matched the previous AntiRecommendations.
        Return an empty tuple if there were no such Records.
        """

        if self.__stack:

            return tuple(self.__stack.pop())

        return ()
