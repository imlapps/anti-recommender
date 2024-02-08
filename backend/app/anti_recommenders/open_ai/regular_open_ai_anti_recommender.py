from typing import Tuple
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableSequence
from langchain.schema import StrOutputParser

from app.anti_recommenders.open_ai.open_ai_anti_recommender import OpenAiAntiRecommender

__all__ = ["RegularOpenAiAntiRecommender"]


class RegularOpenAiAntiRecommender(OpenAiAntiRecommender):
    """A subclass of the OpenAI Anti-Recommender"""

    def _build_model(self) -> RunnableSequence:
        """Build and return an LLM"""

        model = OpenAI()

        try:
            prompt = PromptTemplate.from_template(self.template)
        except Exception:
            self.__logger.warning(
                "Error while building the Langchain OpenAI model. Couldn't generate prompt from PromptTemplate.",
                exc_info=True,
            )
            return 1

        chain = {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()

        return chain

    def _generate_response(self, query: str, chain: RunnableSequence) -> str:
        """Generate response from LLM"""

        response = ""

        try:
            response = chain.invoke(query)
        except Exception:
            self.__logger.warning(
                "Error while generating response from the Langchain OpenAI model.",
                exc_info=True,
            )

            return 1

        return response

    def _parse_response(self, response: str) -> Tuple[Tuple[str, ...], ...]:
        """Extract alternate articles from the LLMs and return a list of anti-recommendations"""

        response_list = response.strip().split("\n")
        alternate_articles = []

        for line in response_list:
            line_chunk = line.split("-")

            if len(line_chunk) < 2:
                continue

            title = line_chunk[1].strip()

            url = ""
            if "wikipedia" in line_chunk[-1]:
                url = line_chunk[-1].strip()

            alternate_articles.append((title, url))

        return tuple(alternate_articles)

    def generate_anti_recommendations(
        self, wikipedia_title: str
    ) -> Tuple[Tuple[str, ...], ...]:
        """Returns a tuple of anti-recommendations for the given wikipedia title"""

        chain = self._build_model()

        query = self._create_query(wikipedia_title)

        response = self._generate_response(query, chain)

        parsed_response = self._parse_response(response)

        return parsed_response
