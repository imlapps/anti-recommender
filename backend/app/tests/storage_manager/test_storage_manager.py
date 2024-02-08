import pytest

from app.storage_manager.storage.storage import Storage
from app.data.wikipedia_output_path import wikipedia_output_path
from app.anti_recommenders.anti_recommender_proxy import AntiRecommenderProxy


class TestStorageManagerInitialization:
    """
    This class contains a suite of tests that ensure that the StorageManager successfully initializes its variables.
    """

    # Test initialize_wikipedia_data method
    def test_initialize_wikipedia_data(
        self,
        class_mocker,
        storage_manager,
    ):
        """
        Test that the StorageManager.initialize_wikipedia_data() calls both Storage.read_wikipedia_data()
        and Storage.set_current_title_to_first_item_title() once.
        """
        class_mocker.patch.object(Storage, "read_wikipedia_data")
        class_mocker.patch.object(Storage, "set_current_title_to_first_item_title")

        storage_manager.initialize_wikipedia_data()

        Storage.read_wikipedia_data.assert_called_once_with(wikipedia_output_path)
        Storage.set_current_title_to_first_item_title.assert_called_once_with()


class TestRetrieveWikipediaArticleMethods:
    """
    This class contains a suite of tests that ensure that the StorageManager successfully retrieves Wikipedia articles from Storage.
    """

    @pytest.fixture(scope="class", autouse=True)
    def initialize(self, storage_manager):
        """This fixture calls the StorageManager.intialize_wikipedia_data() method."""

        storage_manager.initialize_wikipedia_data()

    @pytest.fixture(scope="class")
    def generated_anti_recommendations(self):
        """This fixture returns mock anti_recommendation articles for tests."""

        return tuple(
            [("test-wikipedia-article-1", "https://en.wikipedia.org/wiki/Title")]
        )

    class TestRetrieveCurrentWikipediaArticleMethod:
        """
        This class contains a suite of tests that ensure that StorageManager.retrieve_current_wikipedia_article()
        works as expected.
        """

        def test_retrieve_current_wikipedia_article(
            self, storage_manager, current_wikipedia_record_data
        ):
            """
            Test that StorageManager.retrieve_current_wikipedia_article() successfully retrieves current Wikipedia articles.
            """
            assert (
                storage_manager.retrieve_current_wikipedia_article()
                == current_wikipedia_record_data
            )

    class TestRetrieveNextWikipediaArticlesMethod:
        """
        This class contains a suite of tests that ensure that StorageManager.retrieve_next_wikipedia_articles()
        works as expected.
        """

        def test_retrieve_next_wikipedia_articles(
            self,
            class_mocker,
            storage_manager,
            generated_anti_recommendations,
            current_wikipedia_record_data,
        ):
            """
            Test that StorageManager.retrieve_next_wikipedia_articles() successfully
            returns a tuple of Wikipedia articles when an anti-recommender returns anti-recommendations.
            """

            # Mock the AntiRecommenderProxy.generate_anti_recommendations() and return mock anti-recommendation values.
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
            """
            Test that StorageManager.retrieve_next_wikipedia_articles()
            returns an empty dictionary in an empty tuple when an anti-recommender does not return any anti-recommendations.
            """

            # Mock AntiRecommenderProxy.generate_anti_recommendations() and return mock anti-recommendation values.
            class_mocker.patch.object(
                AntiRecommenderProxy,
                "generate_anti_recommendations",
                return_value=tuple([]),
            )

            assert storage_manager.retrieve_next_wikipedia_articles(
                AntiRecommenderProxy
            ) == tuple([{"anti_recommendations": tuple([{}])}])

    class TestRetrievePreviousWikipediaArticlesMethod:
        """
        This class contains a suite of tests that ensure that StorageManager.retrieve_previous_wikipedia_articles()
        works as expected.
        """

        def test_retrieve_previous_wikipedia_articles(
            self, class_mocker, storage_manager, current_wikipedia_record_data
        ):
            """
            Test that StorageManager.retrieve_previous_wikipedia_articles() successfully
            returns a tuple containing a Wikipedia article if there was a title present in the stack.
            """

            # Mock Storage.pop_title_from_stack() and return sample Wikipedia article title.
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
            """
            Test that StorageManager.retrieve_previous_wikipedia_articles()
            returns an empty dict in an empty tuple if there was no title present in the stack.
            """

            # Mock Storage.pop_title_from_stack() and return an empty string.
            class_mocker.patch.object(Storage, "pop_title_from_stack", return_value="")

            assert storage_manager.retrieve_previous_wikipedia_article() == tuple(
                [{"": ""}]
            )
