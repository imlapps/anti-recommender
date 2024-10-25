from pathlib import Path

from app.models import Record
from app.readers import AllSourceReader


def test_read(
    all_source_reader: AllSourceReader,
    wikipedia_output_file_path: Path,  # noqa: ARG001
) -> None:
    """Test that AllSourceReader.read yields the expected output type."""

    assert isinstance(next(iter(all_source_reader.read())), Record)
