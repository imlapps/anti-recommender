import pytest

from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence


from app.anti_recommenders.open_ai.regular_open_ai_anti_recommender import (
    RegularOpenAiAntiRecommender,
)


OPEN_AI_MODEL_NAME = "gpt-3.5-turbo-instruct"
SAMPLE_TITLE = "test_title"
SAMPLE_QUERY = "test-query"
SAMPLE_MODEL_RESPONSE = "1 - Title - https://en.wikipedia.org/wiki/Title"
SAMPLE_PARSED_MODEL_RESPONSE = tuple([("Title", "https://en.wikipedia.org/wiki/Title")])


@pytest.fixture(scope="class")
def call_regular_open_ai_anti_recommender():
    return RegularOpenAiAntiRecommender()


class TestBuildModel:

    def test_build_model_success(self, call_regular_open_ai_anti_recommender):
        chain = call_regular_open_ai_anti_recommender._build_model()

        assert chain.middle[1].model_name == OPEN_AI_MODEL_NAME

    def test_raises_failed_prompt_creation_exception(
        self, call_regular_open_ai_anti_recommender, mocker
    ):

        # Mock PromptTemplate's from_template method and return an Exception
        mocker.patch.object(PromptTemplate, "from_template", return_value=Exception)

        with pytest.raises(Exception):
            call_regular_open_ai_anti_recommender._build_model()


class TestCreateQuery:

    def test_create_query_success(self, call_regular_open_ai_anti_recommender):

        query = call_regular_open_ai_anti_recommender._create_query(SAMPLE_TITLE)

        assert SAMPLE_TITLE in query


class TestGenerateResponse:

    @pytest.fixture(scope="class")
    def create_generate_response_param(self, call_regular_open_ai_anti_recommender):

        return tuple(
            [SAMPLE_QUERY, call_regular_open_ai_anti_recommender._build_model()]
        )

    def test_generate_response(
        self,
        call_regular_open_ai_anti_recommender,
        create_generate_response_param,
        mocker,
    ):

        # Mock RunnableSerializable's invoke method and return an LLM response
        mocker.patch.object(
            RunnableSequence,
            "invoke",
            return_value=SAMPLE_MODEL_RESPONSE,
        )

        response = call_regular_open_ai_anti_recommender._generate_response(
            *create_generate_response_param
        )

        assert response == SAMPLE_MODEL_RESPONSE

    def test_raises_failed_chain_invocation_exception(
        call_regular_open_ai_anti_recommender, create_generate_response_param, mocker
    ):

        # Mock RunnableSerializable's invoke method and return an Exception
        mocker.patch.object(RunnableSequence, "invoke", return_value=Exception)

        with pytest.raises(Exception):
            call_regular_open_ai_anti_recommender._generate_response(
                *create_generate_response_param
            )


class TestParseResponse:

    def test_parse_response(self, call_regular_open_ai_anti_recommender):

        assert (
            call_regular_open_ai_anti_recommender._parse_response(SAMPLE_MODEL_RESPONSE)
            == SAMPLE_PARSED_MODEL_RESPONSE
        )


class TestGenerateAntiRecommendations:
    def test_generate_anti_recommendations(
        self, mocker, call_regular_open_ai_anti_recommender
    ):

        # Mock RegularOpenAiAntiRecommender's _parse_response method and return a sample response
        mocker.patch.object(
            RegularOpenAiAntiRecommender,
            "_generate_response",
            return_value=SAMPLE_MODEL_RESPONSE,
        )

        assert (
            call_regular_open_ai_anti_recommender.generate_anti_recommendations(
                SAMPLE_TITLE
            )
            == SAMPLE_PARSED_MODEL_RESPONSE
        )