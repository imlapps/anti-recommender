from collections.abc import Iterable

from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain_openai import OpenAI

from app.anti_recommenders.open_ai.open_ai_anti_recommender import OpenAiAntiRecommender
from app.models.anti_recommendation import AntiRecommendation


class NormalOpenAiAntiRecommender(OpenAiAntiRecommender):
    """
    A subclass of OpenAiAntiRecommender that relies solely on
    the large language model's parametric knowledge to generate AntiRecommendations.

    record_type is the type of AntiRecommendations generated from the large language model.
    """

    def _build_chain(self) -> RunnableSerializable:
        """Build a chain that consists of an OpenAI prompt, large language model and an output parser."""

        model = OpenAI()

        prompt = PromptTemplate.from_template(self._template)

        return {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()

    def _generate_llm_response(
        self, query: str, open_ai_chain: RunnableSerializable
    ) -> str:
        """Invoke the OpenAI large language model and generate a response."""

        return open_ai_chain.invoke(query)

    def _parse_llm_response(
        self, open_ai_llm_response: str
    ) -> Iterable[AntiRecommendation]:
        """Extract anti-recommendations from the response and yield AntiRecommendations."""

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

            yield AntiRecommendation(key=title, url=url)

    def generate_anti_recommendations(
        self,
        record_key: str,
        record_type: str,
    ) -> Iterable[AntiRecommendation]:
        """Yield AntiRecommendations of a given record key, and of type record_type."""

        yield from self._generate_anti_recommendendations(
            record_key,
            record_type,
            self._build_chain,
            self._create_query,
            self._generate_llm_response,
            self._parse_llm_response,
        )
