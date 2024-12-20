import typing
from collections.abc import Iterable

from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain_openai import OpenAI
from pydantic import AnyUrl

from app.anti_recommenders.openai import OpenaiAntiRecommender
from app.models import AntiRecommendation
from app.models.types import NonBlankString as ModelQuery
from app.models.types import NonBlankString as ModelResponse
from app.models.types import RecordKey, RecordType


class NormalOpenaiAntiRecommender(OpenaiAntiRecommender):
    """
    A subclass of OpenaiAntiRecommender.

    A NormalOpenaiAntiRecommender relies solely on the large language model's parametric knowledge to generate anti-recommendations.
    """

    def _build_chain(self) -> RunnableSerializable:
        """Build a chain that consists of an OpenAI prompt, large language model and an output parser."""

        model = OpenAI()

        prompt = PromptTemplate.from_template(self._template)

        return {"question": RunnablePassthrough()} | prompt | model | StrOutputParser()

    def _generate_llm_response(
        self, open_ai_query: ModelQuery, open_ai_chain: RunnableSerializable
    ) -> ModelResponse:
        """Invoke the OpenAI large language model and generate a response."""

        return str(open_ai_chain.invoke(open_ai_query))

    def _parse_llm_response(
        self, open_ai_llm_response: ModelResponse
    ) -> Iterable[AntiRecommendation]:
        """Extract anti-recommendations from open_ai_llm_response, and yield anti-recommendations."""

        model_response_length = 3

        response_list = open_ai_llm_response.strip().split("\n")

        for line in response_list:
            line_chunk = line.strip().split("-")

            if len(line_chunk) != model_response_length:
                continue

            title = line_chunk[1].strip()

            url = ""
            if RecordType.WIKIPEDIA in line_chunk[2]:
                url = line_chunk[2].strip()

            yield AntiRecommendation(key=title, url=AnyUrl(url))

    @typing.override
    def generate_anti_recommendations(
        self, *, record_key: RecordKey
    ) -> Iterable[AntiRecommendation]:
        """Yield anti-recommendations of a given record_key."""

        yield from self._generate_anti_recommendendations(
            record_key=record_key,
            build_chain=self._build_chain,
            create_query=self._create_query,
            generate_llm_response=self._generate_llm_response,
            parse_llm_response=self._parse_llm_response,
        )
