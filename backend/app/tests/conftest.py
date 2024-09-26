from collections.abc import Collection
from pathlib import Path
from typing import Any

import pytest
from pyoxigraph import NamedNode
from pytest_mock import MockFixture

from app.anti_recommendation_engine import AntiRecommendationEngine
from app.anti_recommenders.arkg import ArkgAntiRecommender
from app.anti_recommenders.open_ai import NormalOpenAiAntiRecommender
from app.models import (
    WIKIPEDIA_BASE_URL,
    AntiRecommendation,
    Record,
    wikipedia,
    AntiRecommendationGraph,
)
from app.models.types import ModelResponse, RdfMimeType, RecordKey, RecordType
from app.readers import AllSourceReader
from app.readers.reader import WikipediaReader


@pytest.fixture(scope="session")
def all_source_reader() -> AllSourceReader:
    """Return an AllSourceReader object."""

    return AllSourceReader()


@pytest.fixture(scope="session")
def wikipedia_output_path() -> Path:
    """Return the Path of the Wikipedia output file."""

    return (
        Path(__file__).parent.parent.absolute() / "data" / "mini-wikipedia.output.txt"
    )


@pytest.fixture(scope="session")
def wikipedia_reader(wikipedia_output_path: Path) -> WikipediaReader:
    """Return a WikipediaReader object."""

    return WikipediaReader(file_path=wikipedia_output_path)


@pytest.fixture(scope="session")
def open_ai_normal_anti_recommender() -> NormalOpenAiAntiRecommender:
    """Return an OpenAiNormalAntiRecommender object."""
    return NormalOpenAiAntiRecommender()


@pytest.fixture(scope="session")
def record_key() -> RecordKey:
    """Return a sample record key."""

    return "Nikola_Tesla"


@pytest.fixture(scope="session")
def record_type() -> RecordType:
    """Return a sample record type."""

    return RecordType.WIKIPEDIA


@pytest.fixture(scope="session")
def model_response() -> ModelResponse:
    """Return a sample response from a large language model."""

    return "1 - Laplace's_demon - https://en.wikipedia.org/wiki/Laplace's_demon\n\
            2 - Leonardo_da_Vinci - https://en.wikipedia.org/wiki/Leonardo_da_Vinci"


@pytest.fixture(scope="session")
def anti_recommendations() -> tuple[AntiRecommendation, ...]:
    """Return a tuple of anti-recommendations."""

    return (
        AntiRecommendation(
            key="Laplace's_demon",
            url="https://en.wikipedia.org/wiki/Laplace's_demon",
        ),
        AntiRecommendation(
            key="Leonardo_da_Vinci",
            url="https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
        ),
    )


@pytest.fixture(scope="session")
def serialized_records() -> tuple[dict[str, Collection[Collection[str]]], ...]:
    """Return a tuple of serialized records."""

    return (
        {
            "abstract_info": {
                "title": "Nikola_Tesla",
                "abstract": "A Serbian-American inventor, best known for his contributions to the design of \
                             the modern alternating current (AC) electricity supply system.",
                "url": "https://en.wikipedia.org/wiki/Nikola_Tesla",
            },
            "categories": (
                {
                    "text": "Nikola Tesla",
                    "link": "https://en.wikipedia.org/wiki/Category:Nikola_Tesla",
                },
                {
                    "text": "1856 Births",
                    "link": "https://en.wikipedia.org/wiki/Category:1856_births",
                },
                {
                    "text": "19th-century American engineers",
                    "link": "https://en.wikipedia.org/wiki/Category:19th-century_American_engineers",
                },
            ),
            "externallinks": (
                {
                    "title": "Austrian Empire",
                    "link": "https://en.wikipedia.org/wiki/Austrian_Empire",
                },
                {
                    "title": "Electric Power Industry",
                    "link": "https://en.wikipedia.org/wiki/Electric_power_industry",
                },
                {
                    "title": "Telephony",
                    "link": "https://en.wikipedia.org/wiki/Telephony",
                },
            ),
        },
        {
            "abstract_info": {
                "title": "Laplace's_demon",
                "abstract": "In the history of science, Laplace's demon was a notable published articulation \
                         of causal determinism on a scientific basis by Pierre-Simon Laplace in 1814.",
                "url": "https://en.wikipedia.org/wiki/Laplace's_demon",
            },
            "categories": (
                {
                    "text": "Pierre-Simon Laplace",
                    "link": "https://en.wikipedia.org/wiki/Category:Pierre-Simon_Laplace",
                },
                {
                    "text": "Determinism",
                    "link": "https://en.wikipedia.org/wiki/Category:Determinism",
                },
                {
                    "text": "Thought experiments",
                    "link": "https://en.wikipedia.org/wiki/Category:Thought_experiments",
                },
            ),
            "externallinks": (
                {
                    "title": "Classical mechanics",
                    "link": "https://en.wikipedia.org/wiki/Classical_mechanics",
                },
                {
                    "title": "History of Science",
                    "link": "https://en.wikipedia.org/wiki/History_of_science",
                },
                {
                    "title": "Momentum",
                    "link": "https://en.wikipedia.org/wiki/Momentum",
                },
            ),
        },
        {
            "abstract_info": {
                "title": "Leonardo_da_Vinci",
                "abstract": "An Italian polymath of the High Renaissance who was active as a painter, \
                                draughtsman, engineer, scientist, theorist, sculptor, and architect.",
                "url": "https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
            },
            "categories": (
                {
                    "text": "Leonardo da Vinci",
                    "link": "https://en.wikipedia.org/wiki/Category:Leonardo_da_Vinci",
                },
                {
                    "text": "1452 births",
                    "link": "https://en.wikipedia.org/wiki/Category:1452_births",
                },
                {
                    "text": "15th-century Italian mathematicians",
                    "link": "https://en.wikipedia.org/wiki/Category:15th-century_Italian_mathematicians",
                },
            ),
            "externallinks": (
                {"title": "Polymath", "link": "https://en.wikipedia.org/wiki/Polymath"},
                {
                    "title": "High Renaissance",
                    "link": "https://en.wikipedia.org/wiki/High_Renaissance",
                },
                {
                    "title": "Paleontology",
                    "link": "https://en.wikipedia.org/wiki/Paleontology",
                },
            ),
        },
    )


@pytest.fixture(scope="session")
def records(serialized_records: tuple[Any, ...]) -> tuple[Record, ...]:
    """Return a tuple of Records."""

    return tuple(
        wikipedia.Article(**record["abstract_info"], **record)
        for record in serialized_records
    )


@pytest.fixture(scope="session")
def records_by_key(records: tuple[Record, ...]) -> dict[RecordKey, Record]:
    """Return a dictionary of Records."""
    _records_by_key = {}

    for record in records:
        _records_by_key[record.key] = record

    return _records_by_key


@pytest.fixture(scope="session")
def anti_recommendation_engine(
    session_mocker: MockFixture, records: tuple[Record, ...]
) -> AntiRecommendationEngine:
    """Return an AntiRecommendationEngine object."""

    session_mocker.patch.object(AllSourceReader, "read", return_value=records)

    return AntiRecommendationEngine()


@pytest.fixture(scope="session")
def arkg_file_path() -> Path:
    """Return the file path of a Wikipedia ARKG."""

    return Path(__file__).parent.parent.absolute() / "data" / "wikipedia_arkg.ttl"


@pytest.fixture(scope="session")
def arkg_mime_type() -> RdfMimeType:
    """Return the MIME Type of a Wikipedia ARKG file."""

    return RdfMimeType.TURTLE


@pytest.fixture(scope="session")
def arkg_base_iri() -> NamedNode:
    """Return the base IRI of a Wikipedia ARKG."""

    return NamedNode("http://imlapps.github.io/anti-recommender/anti-recommendation/")


@pytest.fixture(scope="session")
def arkg_anti_recommender(
    arkg_base_iri: NamedNode,
    arkg_file_path: Path,
    arkg_mime_type: RdfMimeType,
    records_by_key: dict[RecordKey, Record],
) -> ArkgAntiRecommender:
    """Return an ArkgAntiRecommender object."""

    return ArkgAntiRecommender(
        arkg_base_iri=arkg_base_iri,
        arkg_file_path=arkg_file_path,
        arkg_mime_type=arkg_mime_type,
        record_keys=records_by_key.keys(),
    )
