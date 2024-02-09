import pytest
from app.storage_manager.storage.storage import Storage


@pytest.fixture(scope="class")
def storage():
    """
    This fixture yields a Storage object.
    """

    _storage = Storage()

    yield _storage

    _storage.reset()
