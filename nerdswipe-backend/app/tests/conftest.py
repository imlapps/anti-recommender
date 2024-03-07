from typing import Any
import pytest
from collections.abc import Collection
from pathlib import Path
from pytest_mock import MockFixture

from app.utils.config.config import config
from app.readers.all_source_reader import AllSourceReader
from app.readers.reader.wikipedia_reader.wikipedia_reader import WikipediaReader
from app.anti_recommendation_engine.anti_recommendation_engine import (
    AntiRecommendationEngine,
)
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from app.models.record.record import Record
from app.anti_recommenders.open_ai.open_ai_normal_anti_recommender.open_ai_normal_anti_recommender import (
    OpenAiNormalAntiRecommender,
)
from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy


@pytest.fixture()
def all_source_reader() -> AllSourceReader:
    """Yield an AllSourceReader object."""
    return AllSourceReader()


@pytest.fixture()
def wikipedia_output_path() -> Path | None:
    """Return the Path of the Wikipedia output file."""

    file_name = config[0].get("WIKIPEDIA_OUTPUT_FILE_NAME", None)

    if file_name:
        return Path(__file__).parent.parent / "data" / file_name

    return None


@pytest.fixture()
def wikipedia_reader(wikipedia_output_path: Path) -> WikipediaReader:
    """Yield a WikipediaReader object."""

    return WikipediaReader(file_path=wikipedia_output_path)


@pytest.fixture()
def anti_recommender_proxy() -> AntiRecommenderProxy:
    """Yield an AntiRecommenderProxy object."""

    return AntiRecommenderProxy()


@pytest.fixture()
def open_ai_normal_anti_recommender() -> OpenAiNormalAntiRecommender:
    """Yield an OpenAiNormalAntiRecommender object."""
    return OpenAiNormalAntiRecommender()


@pytest.fixture()
def record_key() -> str:
    """Return a sample record key."""

    return "Nikola Tesla"


@pytest.fixture()
def model_response() -> str:
    """Return a sample response from a large language model."""

    return "1 - Laplace's Demon - https://en.wikipedia.org/wiki/Laplace's_demon\n\
            2 - Leonardo da Vinci - https://en.wikipedia.org/wiki/Leonardo_da_Vinci"


@pytest.fixture()
def anti_recommendations() -> tuple[AntiRecommendation, ...]:
    """Return a tuple of anti-recommendations."""

    return (
        AntiRecommendation(
            title="Laplace's Demon",
            url="https://en.wikipedia.org/wiki/Laplace's_demon",
        ),
        AntiRecommendation(
            title="Leonardo da Vinci",
            url="https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
        ),
    )


@pytest.fixture()
def anti_recommendation() -> tuple[AntiRecommendation, ...]:
    """Yield a single anti-recommendation."""

    return (
        AntiRecommendation(
            title="Laplace's Demon",
            url="https://en.wikipedia.org/wiki/Laplace's_demon",
        ),
    )


@pytest.fixture()
def serialized_records() -> tuple[dict[str, Collection[Collection[str]]], ...]:
    """Return a tuple of serialized records."""

    return (
        {
            "abstract_info": {
                "title": "Nikola Tesla",
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
                "title": "Laplace's Demon",
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
                "title": "Leonardo da Vinci",
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


@pytest.fixture()
def records(serialized_records: tuple[Any, ...]) -> tuple[Record, ...]:
    """Return a tuple of Records."""
    return tuple(Record(**record) for record in serialized_records)


@pytest.fixture()
def record_store(records: tuple[Record, ...]) -> tuple[dict[str, Record], ...]:
    """Return a tuple containing a dictionary of Records."""
    _record_store = {}

    for record in records:
        _record_store[record.abstract_info.title] = record

    return (_record_store,)


@pytest.fixture()
def anti_recommendation_engine_with_mocked_load_records(
    mocker: MockFixture, record_store: tuple[dict[str, Record], ...]
) -> AntiRecommendationEngine:
    """Yield an AntiRecommendationEngine object and mock AntiRecommendationEngine.load_records()."""
    mocker.patch.object(
        AntiRecommendationEngine, "load_records", return_value=record_store
    )

    return AntiRecommendationEngine()


@pytest.fixture()
def anti_recommendation_engine() -> AntiRecommendationEngine:
    """Yield an AntiRecommendationEngine object."""

    return AntiRecommendationEngine()
