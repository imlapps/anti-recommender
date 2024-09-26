import typing
from collections.abc import Iterable
from pathlib import Path

import pyoxigraph as ox

from app.anti_recommenders import AntiRecommender
from app.models import WIKIPEDIA_BASE_URL, AntiRecommendation, AntiRecommendationGraph
from app.models.types import RdfMimeType, RecordKey, StoreQuery
from app.namespaces import SCHEMA


class ArkgAntiRecommender(AntiRecommender):
    """
    A concrete implementation of AntiRecommender.

    ArkgAntiRecommender uses information stored in an Anti-Recommendation Knowledge Graph to generate AntiRecommendations.
    """

    def __init__(
        self,
        *,
        arkg_base_iri: ox.NamedNode,
        arkg_file_path: Path,
        arkg_mime_type: RdfMimeType,
        record_keys: tuple[RecordKey, ...],
    ) -> None:
        self.__anti_recommendation_path_graph: list[AntiRecommendationGraph] = []
        self.__arkg_base_iri = arkg_base_iri
        self.__arkg_file_path = arkg_file_path
        self.__arkg_mime_type = arkg_mime_type
        self.__record_keys: tuple[RecordKey, ...] = record_keys
        self.__store: ox.Store = ox.Store()
        self.__load_store()

    def __create_query(self, record_key: RecordKey) -> StoreQuery:
        """
        Return a SPARQL query that fetches anti-recommendations of `record_key` from an ARKG Store.
        """

        return f"SELECT ?title WHERE {{ <{record_key}> <{SCHEMA.ITEM_REVIEWED.value}> ?resource {{?resource <{SCHEMA.TITLE.value}> ?title}} }}"

    def __build_anti_recommendation_path_graph(
        self, starting_record_key: RecordKey
    ) -> tuple[AntiRecommendationGraph, ...]:
        """
        Return an a tuple of `AntiRecommendationGraphs`.

        The tuple of `AntiRecommendationGraphs` represents a path graph that has been extracted from an ARKG Store.

        The starting point of the path graph is `starting_record_key`.
        """

        graph_head: RecordKey | None = starting_record_key
        anti_recommendation_path_graph: list[AntiRecommendationGraph] = []
        anti_recommendation_path_graph_record_keys: list[RecordKey] = []
        record_keys_list = list(self.__record_keys)

        record_keys_list.sort()

        while record_keys_list:
            anti_recommendation_path_graph_record_keys.append(str(graph_head))
            record_keys_list.remove(str(graph_head))

            anti_recommendation_keys = [
                binding["title"].value
                for binding in self.__store.query(  # type: ignore[union-attr]
                    query=self.__create_query(str(graph_head)),
                    base_iri=self.__arkg_base_iri.value,
                )
            ]

            if anti_recommendation_keys:
                anti_recommendation_path_graph = list(
                    self.__populate_anti_recommendation_path_graph(
                        record_key=str(graph_head),
                        anti_recommendation_path_graph=tuple(
                            anti_recommendation_path_graph
                        ),
                        anti_recommendation_keys=tuple(anti_recommendation_keys),
                    )
                )
                graph_head = None

                # Set graph_head to the first record_key that is not in the path graph
                for anti_recommendation_key in anti_recommendation_keys:
                    if (
                        anti_recommendation_key
                        not in anti_recommendation_path_graph_record_keys
                    ):
                        graph_head = anti_recommendation_key
                        break
            else:
                # If no anti-recommendation keys are in the Store, use the first key in record_keys_list as the anti-recommendation key.
                anti_recommendation_key = record_keys_list.pop(0)
                anti_recommendation_path_graph = list(
                    self.__populate_anti_recommendation_path_graph(
                        record_key=str(graph_head),
                        anti_recommendation_path_graph=tuple(
                            anti_recommendation_path_graph
                        ),
                        anti_recommendation_keys=(anti_recommendation_key,),
                    )
                )
                graph_head = None

            if not graph_head and record_keys_list:
                graph_head = record_keys_list.pop(0)

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
        """Add an `AntiRecommendationGraph` to an anti-recommendation path graph."""

        anti_recommendation_path_graph_list = list(anti_recommendation_path_graph)
        anti_recommendation_path_graph_list.append(
            AntiRecommendationGraph(
                record_key=record_key,
                anti_recommendations=tuple(
                    AntiRecommendation(
                        key=anti_recommendation_key,
                        url=WIKIPEDIA_BASE_URL + anti_recommendation_key,
                    )
                    for anti_recommendation_key in anti_recommendation_keys
                ),
            )
        )

        return tuple(anti_recommendation_path_graph_list)

    @typing.override
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """
        Generate anti-recommendations of a Record.

        Anti-recommendations are obtained from an ARKG.
        """

        if not self.__anti_recommendation_path_graph:
            self.__anti_recommendation_path_graph = list(
                self.__build_anti_recommendation_path_graph(record_key)
            )

        return self.__anti_recommendation_path_graph.pop().anti_recommendations
