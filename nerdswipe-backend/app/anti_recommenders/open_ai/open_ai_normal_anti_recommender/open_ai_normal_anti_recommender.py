from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain.schema import StrOutputParser

from collections.abc import Generator
from app.anti_recommenders.open_ai.open_ai_anti_recommender import OpenAiAntiRecommender
from app.models.anti_recommendation.anti_recommendation import AntiRecommendation


class OpenAiNormalAntiRecommender(OpenAiAntiRecommender):
    def __init__(self) -> None:
        super().__init__()
        self.open_ai_normal_chain: RunnableSerializable | None = None

    def build_chain(self) -> None:
        """Build a chain that consists of an OpenAI prompt, large language model and an output parser."""

        model = OpenAI()

        prompt = PromptTemplate.from_template(self._template)

        self.open_ai_normal_chain = (
            {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()
        )

    def generate_response(self, query: str) -> str | None:
        """Invoke the OpenAI Large Language Model and generate a response."""

        if self.open_ai_normal_chain:
            return self.open_ai_normal_chain.invoke(query)

        return None

    def parse_response(
        self, response: str
    ) -> Generator[AntiRecommendation, None, None]:
        """Extract anti-recommendations from the response and yield AntiRecommendation records."""

        model_response_length = 3

        response_list = response.strip().split("\n")

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

        self.build_chain()
        query = self.create_query(record_key)
        response = self.generate_response(query)

        if response:
            yield from self.parse_response(response)
