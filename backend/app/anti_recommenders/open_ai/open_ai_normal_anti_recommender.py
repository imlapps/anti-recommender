from typing import Any
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain.schema import StrOutputParser

from collections.abc import Generator
from app.anti_recommenders.open_ai.open_ai_anti_recommender import OpenAiAntiRecommender
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation


class OpenAiNormalAntiRecommender(OpenAiAntiRecommender):
    """
    A subclass of OpenAiAntiRecommender that relies solely on
    the large language model's parametric knowledge to generate anti-recommendations.
    """

    def __init__(self) -> None:
        super().__init__()

    def _build_chain(self) -> RunnableSerializable[Any, str]:
        """Build a chain that consists of an OpenAI prompt, large language model and an output parser."""

        model = OpenAI()

        prompt = PromptTemplate.from_template(self._template)

        return {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()

    def _generate_llm_response(
        self, query: str, open_ai_chain: RunnableSerializable[Any, str]
    ) -> str:
        """Invoke the OpenAI Large Language Model and generate a response."""

        return open_ai_chain.invoke(query)

    def _parse_llm_response(
        self, open_ai_llm_response: str
    ) -> Generator[AntiRecommendation, None, None]:
        """Extract anti-recommendations from the response and yield AntiRecommendation records."""

        model_response_length = 3

        response_list = open_ai_llm_response.strip().split("\n")

        for line in response_list:
            line_chunk = line.strip().split("-")

            if len(line_chunk) != model_response_length:
                continue

            title = line_chunk[1].strip()

            url = ""
            if "wikipedia" in line_chunk[2]:
                url = line_chunk[2].strip()

            yield AntiRecommendation(title=title, url=url)

    def generate_anti_recommendations(
        self, record_key: str
    ) -> Generator[AntiRecommendation, None, None]:
        """Yield anti-recommendations of a given record key."""

        yield from self._generate_anti_recommendendations(
            record_key,
            self._build_chain,
            self._create_query,
            self._generate_llm_response,
            self._parse_llm_response,
        )
