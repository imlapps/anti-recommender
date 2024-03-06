from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableSequence
from langchain.schema import StrOutputParser

from typing import Generator
from app.anti_recommender.open_ai.open_ai_anti_recommender import OpenAiAntiRecommender
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation
from langchain.schema.runnable import RunnableSequence


class OpenAiNormalAntiRecommender(OpenAiAntiRecommender):
    def __init__(self) -> None:
        super().__init__()
        self._open_ai_normal_chain: RunnableSequence | None = None

    def _build_chain(self) -> None:
        """Build a chain that consists of an OpenAI prompt, large language model and an output parser."""

        model = OpenAI()

        prompt = PromptTemplate.from_template(self._template)

        self._open_ai_normal_chain = (
            {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()
        )

    def _generate_response(self, query: str) -> str:
        """Invoke the OpenAI Large Language Model and generate a response."""

        return self._open_ai_normal_chain.invoke(query)

    def _parse_response(
        self, response: str
    ) -> Generator[AntiRecommendation, None, None]:
        """Extract anti-recommendations from the response and yield AntiRecommendation records."""

        response_list = response.strip().split("\n")

        for line in response_list:
            line_chunk = line.strip().split("-")

            if len(line_chunk) != 3:
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

        self._build_chain()
        query = self._create_query(record_key)
        response = self._generate_response(query)

        yield from self._parse_response(response)
