
from collections.abc import Generator
from app.models.record import Record
from app.readers.all_source_reader import AllSourceReader
from app.anti_recommenders.anti_recommender import AntiRecommender
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender import OpenAiNormalAntiRecommender
from app.models.settings import settings
from app.models.anti_recommendation import AntiRecommendation


class AntiRecommendationEngine(AntiRecommender):
    """
    The main AntiRecommendationEngine for the NerdSwipe backend.

    """

    def __init__(self) -> None:
        self.__records_by_key: dict[str, Record] = self.load_records()
        self.__anti_recommender: AntiRecommender | None = self.__select_anti_recommender()
        self.__stack: list[list[Record]] = []
        self.__current_anti_recommendation_records: list[Record] = []

    def __select_anti_recommender(self) -> AntiRecommender | None:
        """Return an AntiRecommender based on values stored in settings."""

        if settings.anti_recommender_type.lower() == "openai" and settings.openai_api_key:
            return OpenAiNormalAntiRecommender()

        return None

    def load_records(self) -> dict[str, Record]:
        """Load records from AllSourceReader and store them in __record_store."""

        records = {}
        all_source_reader = AllSourceReader()

        for record in all_source_reader.read():
            records[record.title] = record

        return records

    def generate_initial_anti_recommendation_records(self) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same key as AntiRecommendations of the first key in __records_by_key."""

        record_key = next(iter(self.__records_by_key.keys()))

        return self.generate_anti_recommendation_records(record_key)

    def generate_anti_recommendation_records(
        self, record_key: str
    ) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same key as the AntiRecommendations of record_key."""

        records_of_anti_recommendations: list[Record] = []

        # Retrieve Records that have the same title of the generated AntiRecommendations
        records_of_anti_recommendations = [
            self.__records_by_key[anti_recommendation.title]
            for anti_recommendation in self.generate_anti_recommendations(record_key)
            if anti_recommendation.title in self.__records_by_key
        ]

        if records_of_anti_recommendations:

            if self.__current_anti_recommendation_records:

                self.__stack.append(self.__current_anti_recommendation_records)

            self.__current_anti_recommendation_records = [
                self.__records_by_key[record_key],
                *records_of_anti_recommendations,
            ]

        return tuple(records_of_anti_recommendations)

    def get_previous_anti_recommendation_records(
        self,
    ) -> tuple[Record | None, ...]:
        """Return a tuple of Records that have the same titles as previous AntiRecommendations."""

        if self.__stack:
            return tuple(self.__stack.pop())

        return (None,)

    def generate_anti_recommendations(self, record_key: str) -> Generator[AntiRecommendation, None, None]:
        """Yield AntiRecommendations of record_key."""

        if self.__anti_recommender:
            yield from self.__anti_recommender.generate_anti_recommendations(record_key)
