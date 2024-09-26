from collections.abc import Iterable
from pathlib import Path

import pyoxigraph as ox

from app.anti_recommenders import AntiRecommender
from app.models import WIKIPEDIA_BASE_URL, AntiRecommendation, AntiRecommendationGraph
from app.models.types import RdfMimeType, RecordKey, RecordType
from app.namespaces import SCHEMA


class ArkgAntiRecommender(AntiRecommender):
    """
    A concrete implementation of AntiRecommender that uses an
    Anti-Recommendation Knowledge Graph (ARKG) to generate anti-recommendations.
    """

    def __init__(
        self,
        *,
        arkg_base_iri: ox.NamedNode,
        arkg_file_path: Path,
        arkg_mime_type: RdfMimeType,
        record_keys: tuple[RecordKey, ...],
    ) -> None:
        self.__arkg_base_iri = arkg_base_iri
        self.__arkg_file_path = arkg_file_path
        self.__arkg_mime_type = arkg_mime_type
        self.__record_keys: tuple[RecordKey, ...] = record_keys
        self.__store: ox.Store = ox.Store()
        self.__anti_recommendation_path_graph: list[AntiRecommendationGraph] = []
        self.__load_store()

    def __build_anti_recommendation_path_graph(
        self, head: RecordKey
    ) -> tuple[AntiRecommendationGraph, ...]:
        """Extract a anti-recommendation path graph from an ARKG Store."""

        anti_recommendation_path_graph: list[AntiRecommendationGraph] = []
        anti_recommendation_path_graph_record_keys: list[RecordKey] = []
        record_keys_queue = list(self.__record_keys)
        record_keys_queue.sort()

        while record_keys_queue:
            anti_recommendation_path_graph_record_keys.append(head)
            record_keys_queue.remove(head)

            anti_recommendation_keys = list(
                binding["title"].value
                for binding in self.__store.query(
                    query=f"SELECT ?title WHERE {{ <{head}> <{SCHEMA.ITEM_REVIEWED.value}> ?resource {{?resource <{SCHEMA.TITLE.value}> ?title}} }}",
                    base_iri=self.__arkg_base_iri.value,
                )
            )

            if anti_recommendation_keys:
                anti_recommendation_path_graph = list(
                    self.__populate_anti_recommendation_path_graph(
                        record_key=head,
                        anti_recommendation_path_graph=tuple(
                            anti_recommendation_path_graph
                        ),
                        anti_recommendation_keys=tuple(anti_recommendation_keys),
                    )
                )
                head = None

                for anti_recommendation_key in anti_recommendation_keys:
                    if (
                        anti_recommendation_key
                        not in anti_recommendation_path_graph_record_keys
                    ):
                        head = anti_recommendation_key
                        break
            else:
                anti_recommendation_key = record_keys_queue.pop(0)
                anti_recommendation_path_graph = list(
                    self.__populate_anti_recommendation_path_graph(
                        record_key=head,
                        anti_recommendation_path_graph=tuple(
                            anti_recommendation_path_graph
                        ),
                        anti_recommendation_keys=(anti_recommendation_key,),
                    )
                )
                head = None

            if not head and record_keys_queue:
                head = record_keys_queue.pop(0)

        return tuple(anti_recommendation_path_graph)

    def __load_store(self) -> None:
        """Load an ARKG serialization into an RDF Store."""

        self.__store.load(
            input=self.__arkg_file_path,
            mime_type=self.__arkg_mime_type.value,
            base_iri=self.__arkg_base_iri.value,
        )

    def __populate_anti_recommendation_path_graph(
        self,
        *,
        record_key: RecordKey,
        anti_recommendation_path_graph: tuple[AntiRecommendationGraph, ...],
        anti_recommendation_keys: tuple[RecordKey, ...],
    ) -> tuple[AntiRecommendationGraph, ...]:
        """Add an anti-recommendation graph to an anti-recommendation path graph."""

        anti_recommendation_path_graph_list = list(anti_recommendation_path_graph)
        anti_recommendation_path_graph_list.append(
            AntiRecommendationGraph(
                record_key=record_key,
                anti_recommendations=(
                    AntiRecommendation(
                        key=anti_recommendation_key,
                        url=WIKIPEDIA_BASE_URL + anti_recommendation_key,
                    )
                    for anti_recommendation_key in anti_recommendation_keys
                ),
            )
        )

        return tuple(anti_recommendation_path_graph_list)

    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """
        Generate anti-recommendations of a record.

        Anti-recommendations are obtained from an ARKG.
        """

        if not self.__anti_recommendation_path_graph:
            self.__anti_recommendation_path_graph = list(
                self.__build_anti_recommendation_path_graph(record_key)
            )

        return self.__anti_recommendation_path_graph.pop().anti_recommendations
