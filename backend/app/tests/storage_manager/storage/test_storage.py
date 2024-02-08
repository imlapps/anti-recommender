import pytest
from app.utils.json import json_loader
from app.storage_manager.storage.storage import Storage
from app.data.wikipedia_output_path import wikipedia_output_path


@pytest.fixture(scope="class")
def storage_wikipedia_data():
    return {
        "test-wikipedia-article": {"test-info": "test info for test-wikipedia-article"}
    }


@pytest.fixture(scope="class")
def current_wikipedia_record_data(storage_wikipedia_data):
    return tuple(
        [
            {
                list(storage_wikipedia_data.keys())[0]: storage_wikipedia_data[
                    list(storage_wikipedia_data.keys())[0]
                ]
            }
        ]
    )


@pytest.fixture(scope="class")
def storage_object():
    storage = Storage()

    yield storage

    storage.reset()


class TestReadWikipediaDataFromStorage:

    @pytest.fixture(scope="class", autouse=True)
    def read_wikipedia_data_from_storage(
        self, class_mocker, storage_object, storage_wikipedia_data
    ):
        class_mocker.patch.object(
            json_loader, "load_data", return_value=[storage_wikipedia_data]
        )

        storage_object.read_wikipedia_data(wikipedia_output_path)

    class TestReadWikipediaData:
        def test_read_wikipedia_data(self):
            json_loader.load_data.assert_called_once_with(wikipedia_output_path)

    class TestStorageTitle:
        def test_store_first_title_as_current_title(
            self, storage_wikipedia_data, storage_object
        ):

            storage_object.set_current_title_to_first_item_title()

            assert (
                storage_object.current_title == list(storage_wikipedia_data.keys())[0]
            )

    class TestStorageRecord:
        def test_get_current_record(
            self, storage_object, current_wikipedia_record_data
        ):

            storage_object.set_current_title_to_first_item_title()

            assert storage_object.get_current_record() == current_wikipedia_record_data

        def test_get_article_records(
            self, storage_object, current_wikipedia_record_data
        ):

            assert (
                storage_object.get_article_records("test-wikipedia-article")
                == current_wikipedia_record_data
            )


class TestNoWikipediaDataFromStorage:

    class TestStorageTitle:
        def test_store_first_title_as_current_title_when_wikipedia_data_is_empty(
            self,
            storage_object,
        ):
            storage_object.set_current_title_to_first_item_title()
            assert storage_object.current_title == ""

        def test_current_title(self, storage_object):
            sample_title = "current-title"

            storage_object.current_title = sample_title

            assert storage_object.current_title == sample_title

    class TestStorageStack:
        def test_pop_from_empty_stack(self, storage_object):
            assert storage_object.pop_title_from_stack() == None

        def test_push_to_stack(self, storage_object):
            storage_object.push_title_to_stack(title="test-wikipedia")

            assert "test-wikipedia" == storage_object.pop_title_from_stack()

    class TestResetStorage:
        def test_reset_storage(self, storage_object):
            storage_object.reset()
            storage_object.set_current_title_to_first_item_title()

            assert storage_object.current_title == ""
            assert storage_object.pop_title_from_stack() == None
