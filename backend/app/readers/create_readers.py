from app.models import Settings
from app.readers.reader import Reader, WikipediaReader


def create_readers(settings: Settings) -> tuple[Reader, ...]:
    """Return a tuple of Readers."""

    return tuple(
        [
            WikipediaReader(output_file_path)
            for output_file_path in settings.output_file_paths
        ]
    )
