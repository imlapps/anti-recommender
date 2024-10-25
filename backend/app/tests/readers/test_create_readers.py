from pathlib import Path

from app.models.settings import Settings
from app.readers import create_readers
from app.readers.reader import Reader


def test_create_readers(
    settings: Settings,
    wikipedia_output_file_path: Path,  # noqa: ARG001
) -> None:
    """Test that create_readers returns the expected tuple of Readers."""

    assert isinstance(create_readers(settings)[0], Reader)
