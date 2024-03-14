from typing import Any

from app.anti_recommenders.anti_recommender_generator import AntiRecommendationGenerator
from app.models.record.record import Record
from app.readers.all_source_reader import AllSourceReader


class AntiRecommendationEngine:
    def __init__(self) -> None:
        self.__record_store: tuple[dict[str,
                                        Record], ...] = self.load_records()
        self.__anti_recommender_proxy: AntiRecommendationGenerator = AntiRecommendationGenerator()
        self.__stack: list[tuple[dict[str, Any], ...]] = []
        self.current_anti_recommendations: list[dict[str, Any]] = []

    def load_records(self) -> tuple[dict[str, Record], ...]:
        """Load records from AllSourceReader and store them in __record_store."""

        records = {}
        all_source_reader = AllSourceReader()

        for record in all_source_reader.read():
            records[record.abstract_info.title] = record

        return (records,)

    def generate_anti_recommendations(
        self, record_key: str | None = None
    ) -> tuple[dict[str, dict[str, str]], ...]:
        """Generate anti-recommendations of a record."""

        # Ensure that record_key is initialized
        if not record_key and self.current_anti_recommendations:
            record_key = self.current_anti_recommendations[0]["abstract_info"]["title"]
        elif not record_key:
            record_key = next(iter(self.__record_store[0].keys()))

        anti_recommendations: list[dict[str, dict[str, str]]] = []

        if record_key:
            anti_recommendations = [
                self.__record_store[0][anti_recommendation.title].model_dump()
                for anti_recommendation in self.__anti_recommender_proxy.generate_anti_recommendations(
                    record_key
                )
                if anti_recommendation.title in self.__record_store[0]
            ]

            if anti_recommendations and record_key in self.__record_store[0]:
                # if current_anti_recommendations is not empty, add its contents to the stack
                # and replace it with the serialized main record and new anti-recommendations.
                if self.current_anti_recommendations:
                    self.__stack.append(
                        tuple(self.current_anti_recommendations))
                    self.current_anti_recommendations = [
                        self.__record_store[0][record_key].model_dump(),
                        *anti_recommendations,
                    ]
                else:
                    # if current_anti_recommendations is empty, set its value to the serialized main record and new anti-recommendations.
                    # An empty current_anti_recommendation implies that this is the first batch of anti-recommendations generated, and it
                    # serves to seed the /root endpoint on start-up.
                    self.current_anti_recommendations.extend(
                        [
                            self.__record_store[0][record_key].model_dump(),
                            *anti_recommendations,
                        ]
                    )

        return tuple(anti_recommendations)

    def get_previous_anti_recommendations(
        self,
    ) -> tuple[dict[Any, Any], ...]:
        """Return a tuple that contains previous anti-recommendations."""

        if self.__stack:
            return self.__stack.pop()

        return ({},)
