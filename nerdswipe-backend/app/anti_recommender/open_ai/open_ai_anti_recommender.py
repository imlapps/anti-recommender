from typing import Generator
from abc import abstractmethod
from langchain.schema.runnable import RunnableSequence

from app.anti_recommender.anti_recommender import AntiRecommender
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation


class OpenAiAntiRecommender(AntiRecommender):
    def __init__(self) -> None:
        self._template = """
                Use the following pieces of context to answer the question at the end. 
                If you don't know the answer, just say that you don't know, don't try to make up an answer. 
                Keep the answer as concise as possible. 
                Question: {question}
                Helpful Answer:
                """

    def _create_query(self, record_key: str) -> str:
        """Create a query with the given wikipedia title for the LLM"""

        query = (
            "What are 10 Wikipedia articles on the featured list that are dissimilar but surprisingly similar to the \
                 Wikipedia article "
            + record_key
            + "? \
                 Give each answer on a new line, and in the format: Number - Title - URL."
        )

        return query

    @abstractmethod
    def _build_chain() -> None:
        pass

    @abstractmethod
    def _generate_response(self, query: str, chain: RunnableSequence) -> str:
        pass

    @abstractmethod
    def _parse_response(self, response: str) -> Generator[AntiRecommendation, None, None]:
        pass

    @abstractmethod
    def generate_anti_recommendations(self, record_key: str) -> Generator[AntiRecommendation, None, None]:
        pass
