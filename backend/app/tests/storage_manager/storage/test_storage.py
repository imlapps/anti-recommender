import pytest
from app.utils.json import json_loader

from app.data.wikipedia_output_path import wikipedia_output_path


class TestReadWikipediaDataFromStorage:
    """
    This class contains a suite of tests  to ensure that Storage's methods work as expected when Wikipedia data has been read in.
    """

    @pytest.fixture(scope="class", autouse=True)
    def read_wikipedia_data_from_storage(
        self, class_mocker, storage, storage_wikipedia_data
    ):
        """This is a fixture that reads in Wikipedia data into Storage."""

        # Mock json_loader.load_data() and return a tuple of sample Wikipedia articles.
        class_mocker.patch.object(
            json_loader, "load_data", return_value=[storage_wikipedia_data]
        )

        storage.read_wikipedia_data(wikipedia_output_path)

    class TestReadWikipediaData:
        """This class contains a suite of tests to ensure that Storage.read_wikipedia_data() works as expected."""

        def test_read_wikipedia_data(self):
            """Test that the json_loader.load_data() is called once with a given Wikipedia output path."""

            json_loader.load_data.assert_called_once_with(wikipedia_output_path)

    class TestStorageTitle:
        """This class contains a suite of tests to ensure that Storage.current_title works as expected."""

        def test_store_first_title_as_current_title(
            self, storage_wikipedia_data, storage
        ):
            """Test that Storage correctly sets Storage.current_title when Storage.set_current_title_to_first_item_title() is called."""
            storage.set_current_title_to_first_item_title()

            assert storage.current_title == list(storage_wikipedia_data.keys())[0]

    class TestStorageRecord:
        """This class contains a suite of tests to ensure that the methods used to get Wikipedia records from Storage work as expected."""

        def test_get_current_record(self, storage, current_wikipedia_record_data):
            """Test that Storage.get_current_record() returns the record of the current title in Storage."""
            storage.set_current_title_to_first_item_title()

            assert storage.get_current_record() == current_wikipedia_record_data

        def test_get_article_records(self, storage, current_wikipedia_record_data):
            """Test that Storage.get_article_records() returns the record of a given Wikipedia article."""
            assert (
                storage.get_article_records("test-wikipedia-article-1")
                == current_wikipedia_record_data
            )


class TestNoWikipediaDataFromStorage:
    """
    This class contains a suite of tests that ensure that Storage's methods work as expected when Wikipedia data has not been read in.
    """

    class TestStorageTitle:
        """This class contains a suite of tests to ensure that Storage.current_title works as expected."""

        def test_store_first_title_as_current_title_when_wikipedia_data_is_empty(
            self,
            storage,
        ):
            """Test that Storage correctly sets Storage.current_title when Storage.set_current_title_to_first_item_title() is called."""
            storage.set_current_title_to_first_item_title()
            assert storage.current_title == ""

        def test_current_title(self, storage):
            """Test that Storage correctly sets the Storage.current_title when it is given a title."""

            sample_title = "current-title"

            storage.current_title = sample_title

            assert storage.current_title == sample_title

    class TestStorageStack:
        """This class contains a suite of tests that ensure that Storage's stack works as expected."""

        def test_pop_from_empty_stack(self, storage):
            """Test that Storage.pop_title_from_stack() returns None when there is no title on the stack."""

            assert storage.pop_title_from_stack() == None

        def test_push_to_stack(self, storage):
            """Test that the title popped from the stack, matches the first item pushed onto the stack."""

            storage.push_title_to_stack(title="test-wikipedia")

            assert "test-wikipedia" == storage.pop_title_from_stack()

    class TestResetStorage:
        """This class contains a suite of tests that ensure that Storage.reset() works as expected."""

        def test_reset_storage(self, storage):
            """Test that the variables of Storage are cleared successfully when Storage.reset() is called."""

            storage.reset()
            storage.set_current_title_to_first_item_title()

            assert storage.current_title == ""
            assert storage.pop_title_from_stack() == None
