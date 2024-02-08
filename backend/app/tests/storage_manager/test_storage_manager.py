import pytest

from app.storage_manager.storage.storage import Storage
from app.data.wikipedia_output_path import wikipedia_output_path
from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy


class TestStorageManagerInitialization:

    # Test initialize_wikipedia_data method
    def test_initialize_wikipedia_data(
        self,
        class_mocker,
        storage_manager,
    ):

        class_mocker.patch.object(Storage, "read_wikipedia_data")
        class_mocker.patch.object(Storage, "set_current_title_to_first_item_title")

        storage_manager.initialize_wikipedia_data()

        Storage.read_wikipedia_data.assert_called_once_with(wikipedia_output_path)
        Storage.set_current_title_to_first_item_title.assert_called_once_with()


class TestRetrieveWikipediaArticleMethods:

    @pytest.fixture(scope="class", autouse=True)
    def initialize(self, storage_manager):
        storage_manager.initialize_wikipedia_data()

    @pytest.fixture(scope="class")
    def generated_anti_recommendations(self):
        return tuple(
            [("test-wikipedia-article-1", "https://en.wikipedia.org/wiki/Title")]
        )

    class TestRetrieveCurrentWikipediaArticleMethod:
        def test_retrieve_current_wikipedia_article(
            self, storage_manager, current_wikipedia_record_data
        ):
            assert (
                storage_manager.retrieve_current_wikipedia_article()
                == current_wikipedia_record_data
            )

    class TestRetrieveNextWikipediaArticlesMethod:

        def test_retrieve_next_wikipedia_articles(
            self,
            class_mocker,
            storage_manager,
            generated_anti_recommendations,
            current_wikipedia_record_data,
        ):

            class_mocker.patch.object(
                AntiRecommenderProxy,
                "generate_anti_recommendations",
                return_value=generated_anti_recommendations,
            )

            assert storage_manager.retrieve_next_wikipedia_articles(
                AntiRecommenderProxy
            ) == tuple([{"anti_recommendations": current_wikipedia_record_data}])

        def test_retrieve_empty_next_wikipedia_articles(
            self,
            class_mocker,
            storage_manager,
        ):
            class_mocker.patch.object(
                AntiRecommenderProxy,
                "generate_anti_recommendations",
                return_value=tuple([]),
            )

            assert storage_manager.retrieve_next_wikipedia_articles(
                AntiRecommenderProxy
            ) == tuple([{"anti_recommendations": tuple([{}])}])

    class TestRetrievePreviousWikipediaArticlesMethod:
        def test_retrieve_previous_wikipedia_articles(
            self, class_mocker, storage_manager, current_wikipedia_record_data
        ):

            class_mocker.patch.object(
                Storage, "pop_title_from_stack", return_value="test-wikipedia-article-1"
            )

            assert (
                storage_manager.retrieve_previous_wikipedia_article()
                == current_wikipedia_record_data
            )

        def test_retrieve_empty_previous_wikipedia_articles(
            self, class_mocker, storage_manager
        ):
            class_mocker.patch.object(Storage, "pop_title_from_stack", return_value="")

            assert storage_manager.retrieve_previous_wikipedia_article() == tuple(
                [{"": ""}]
            )
