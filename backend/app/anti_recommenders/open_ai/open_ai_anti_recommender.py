from abc import abstractmethod
from collections.abc import Callable, Iterator
from langchain.schema.runnable import RunnableSerializable
from app.anti_recommenders.anti_recommender import AntiRecommender
from app.models.anti_recommendation import AntiRecommendation
from app.models.types import RecordType


class OpenAiAntiRecommender(AntiRecommender):
    """
    A concrete implementation of AntiRecommender that uses
    OpenAI's large language model to generate AntiRecommendations.
    """

    def __init__(self) -> None:
        self._template = """
                Use the following pieces of context to answer the question at the end.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Keep the answer as concise as possible.
                Question: {question}
                Helpful Answer:
                """

    def _create_query(self, record_key: str, record_type: RecordType) -> str:
        """Create a query for the large language model with the given record key."""

        if record_type is RecordType.WIKIPEDIA:
            return (
                "What are 10 Wikipedia articles on the featured list that are dissimilar but surprisingly similar to the \
                    Wikipedia article "
                + record_key
                + "? \
                    Give each answer on a new line, and in the format: Number - Title - URL."
            )

    def _generate_anti_recommendendations(  # noqa: PLR0913
        self,
        record_key: str,
        record_type: RecordType,
        build_chain: Callable[[], RunnableSerializable],
        create_query: Callable[[str, RecordType], str],
        generate_llm_response: Callable[[str, RunnableSerializable], str],
        parse_llm_response: Callable[[str], Iterator[AntiRecommendation, None, None]],
    ) -> Iterator[AntiRecommendation, None, None]:
        """Create a generalized workflow that yields AntiRecommendations."""

        open_ai_chain = build_chain()
        open_ai_query = create_query(record_key, record_type)
        generate_open_ai_llm_response = generate_llm_response(
            open_ai_chain, open_ai_query
        )

        yield from parse_llm_response(generate_open_ai_llm_response)

    @abstractmethod
    def generate_anti_recommendations(
        self, record_key: str, record_type: RecordType
    ) -> Iterator[AntiRecommendation, None, None]:
        pass
