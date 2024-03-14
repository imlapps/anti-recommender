from app.anti_recommenders.anti_recommender_generator import AntiRecommendationGenerator
from app.models.record.record import Record
from app.readers.all_source_reader import AllSourceReader


class AntiRecommendationEngine:
    """
    The main AntiRecommendationEngine for the NerdSwipe backend.
    It retrieves AntiRecommendations from the AntiRecommendationGenerator and possesses methods
    which return tuples of Records that have the same titles as the generated AntiRecommendations or previous AntiRecommendations.
    """

    def __init__(self) -> None:
        self.__record_store: dict[str, Record] = self.load_records()
        self.__anti_recommendation_generator: AntiRecommendationGenerator = (
            AntiRecommendationGenerator()
        )
        self.__stack: list[list[Record]] = []
        self.__current_anti_recommendation_records: list[Record] = []

    def load_records(self) -> dict[str, Record]:
        """Load records from AllSourceReader and store them in __record_store."""

        records = {}
        all_source_reader = AllSourceReader()

        for record in all_source_reader.read():
            abstract_info = record.abstract_info
            if abstract_info:
                records[abstract_info.title] = record

        return records

    def generate_anti_recommendation_records(
        self, record_key: str | None = None
    ) -> tuple[Record, ...]:
        """Return a tuple of Records that have the same title as the generated AntiRecommendations."""
        records_of_anti_recommendations: list[Record] = []

        # Use key of first Record in __record_store as the record_key
        if not record_key:
            record_key = next(iter(self.__record_store.keys()))

        # Retrieve Records that have the same title of the generated AntiRecommendations
        records_of_anti_recommendations = [
            self.__record_store[anti_recommendation.title]
            for anti_recommendation in self.__anti_recommendation_generator.generate_anti_recommendations(
                record_key
            )
            if anti_recommendation.title in self.__record_store
        ]

        if records_of_anti_recommendations:

            if self.__current_anti_recommendation_records:

                self.__stack.append(self.__current_anti_recommendation_records)

            self.__current_anti_recommendation_records = [
                self.__record_store[record_key],
                *records_of_anti_recommendations,
            ]

        return tuple(records_of_anti_recommendations)

    def get_previous_anti_recommendation_records(
        self,
    ) -> tuple[Record, ...] | None:
        """Return a tuple of Records that have the same titles as previous AntiRecommendations"""

        if self.__stack:
            return tuple(self.__stack.pop())

        return None
