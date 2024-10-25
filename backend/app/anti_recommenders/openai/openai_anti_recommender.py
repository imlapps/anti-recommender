from abc import abstractmethod
from collections.abc import Callable, Iterable

from langchain.schema.runnable import RunnableSerializable

from app.anti_recommenders.anti_recommender import AntiRecommender
from app.models import AntiRecommendation
from app.models.types import NonBlankString as ModelQuery
from app.models.types import NonBlankString as ModelResponse
from app.models.types import RecordKey


class OpenaiAntiRecommender(AntiRecommender):
    """
    A concrete implementation of AntiRecommender.

    An OpenaiAntiRecommender uses OpenAI's large language model to generate anti-recommendations.
    """

    def __init__(self) -> None:
        self._template = """
                Use the following pieces of context to answer the question at the end.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Keep the answer as concise as possible.
                Question: {question}
                Helpful Answer:
                """

    def _create_query(self, record_key: RecordKey) -> ModelQuery:
        """Create a query for the large language model with the given record_key."""

        return (
            "What are 10 Wikipedia articles on the featured list that are dissimilar but surprisingly similar to the \
                    Wikipedia article "
            + record_key
            + "? \
                    Give each answer on a new line, and in the format: Number - Title - URL."
        )

    def _generate_anti_recommendendations(
        self,
        *,
        record_key: RecordKey,
        build_chain: Callable[[], RunnableSerializable],
        create_query: Callable[[RecordKey], ModelQuery],
        generate_llm_response: Callable[
            [ModelQuery, RunnableSerializable], ModelResponse
        ],
        parse_llm_response: Callable[[ModelResponse], Iterable[AntiRecommendation]],
    ) -> Iterable[AntiRecommendation]:
        """Create a generalized workflow that yields anti-recommendations."""

        open_ai_chain = build_chain()
        open_ai_query = create_query(record_key)
        generate_open_ai_llm_response = generate_llm_response(
            open_ai_query, open_ai_chain
        )

        yield from parse_llm_response(generate_open_ai_llm_response)

    @abstractmethod
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """Generate anti-recommendations of a record_key."""
        raise NotImplementedError
