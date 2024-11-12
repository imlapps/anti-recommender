from app.models import Record
from app.readers import AllSourceReader


def test_read(
    all_source_reader: AllSourceReader,
) -> None:
    """Test that AllSourceReader.read yields the expected output type."""

    assert isinstance(next(iter(all_source_reader.read())), Record)
