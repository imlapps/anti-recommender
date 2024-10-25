from app.models.settings import Settings
from app.readers import create_readers
from app.readers.reader import Reader


def test_create_readers(settings: Settings) -> None:
    """Test that create_readers returns the expected tuple of Readers."""

    assert isinstance(create_readers(settings)[0], Reader)
