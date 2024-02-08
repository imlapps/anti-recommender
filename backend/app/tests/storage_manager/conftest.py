import pytest
from app.utils.json import json_loader
from app.storage_manager.storage.storage import Storage
from app.storage_manager.storage_manager import StorageManager
from app.data.wikipedia_output_path import wikipedia_output_path


@pytest.fixture(scope="module")
def storage_wikipedia_data():
    """This fixture returns a dictionary containing sample Wikipedia articles."""

    return {
        "test-wikipedia-article-1": {
            "test-info": "test info for test-wikipedia-article-1"
        },
    }


@pytest.fixture(scope="module")
def current_wikipedia_record_data(storage_wikipedia_data):
    """
    This fixture accesses storage_wikipedia_data and
    returns a tuple that contains the first entry in the fixture.
    """

    return tuple(
        [
            {
                list(storage_wikipedia_data.keys())[0]: storage_wikipedia_data[
                    list(storage_wikipedia_data.keys())[0]
                ]
            }
        ]
    )


@pytest.fixture(scope="module")
def storage(module_mocker, storage_wikipedia_data):
    """
    This fixture yields a Storage object.
    The values of storage_wikipedia_data are read into the Storage object.
    """

    _storage = Storage()

    module_mocker.patch.object(
        json_loader, "load_data", return_value=[storage_wikipedia_data]
    )

    _storage.read_wikipedia_data(wikipedia_output_path)

    yield _storage

    _storage.reset()


@pytest.fixture(scope="module")
def storage_manager(storage):
    """
    This fixture yields a StorageManager object.
    the StorageManager object is initialized with the storage fixture and a default wikipedia output path.
    """
    _storage_manager = StorageManager(storage, wikipedia_output_path)

    yield _storage_manager

    _storage_manager.reset_storage_manager()
