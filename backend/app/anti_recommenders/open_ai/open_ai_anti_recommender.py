import logging 
from typing import Tuple, Any
from abc import abstractmethod
from langchain.schema.runnable import RunnableSerializable
from ..anti_recommender import AntiRecommender


class OpenAiAntiRecommender(AntiRecommender):
    """A concrete implementation of AntiRecommender that uses the OpenAI API."""

    def __init__(self) -> None:
        self.template = """
                        Use the following pieces of context to answer the question at the end. 
                        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
                        Keep the answer as concise as possible. 
                        Question: {question}
                        Helpful Answer:
                        """
        
        self.__logger = logging.getLogger()

    def _create_query(self, wikipedia_title: str) -> str:
        """Create a query with the given wikipedia title for the LLM"""

        query = "What are 10 Wikipedia articles on the featured list that are dissimilar but surprisingly similar to the \
                 Wikipedia article "+ wikipedia_title + "? \
                 Give each answer on a new line, and in the format: Number - Title - URL."
        
        return query
    

    def _get_logger(self) -> Any:
        """Gets the logger for the LLM"""
        return self.__logger

    @abstractmethod
    def _build_model(self) -> RunnableSerializable[Any, str]:
        pass

    @abstractmethod
    def _generate_response(self, query: str, chain) -> str:
        pass
    
    @abstractmethod
    def _parse_response(self, response: str) -> Tuple[Tuple[str, ...], ...]:
        pass 

    @abstractmethod
    def generate_anti_recommendations(self, wikipedia_title: str  = "") -> Tuple[Tuple[str, ...], ...]:
        pass 