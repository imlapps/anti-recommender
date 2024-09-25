from app.models import Settings
from app.models.types import RecordType
from app.readers.reader import Reader, WikipediaReader


def create_readers(settings: Settings) -> tuple[Reader, ...]:
    """
    Return a tuple of Readers depending on the record type in settings.
    Readers are instantiated with Paths that contain the corresponding record types in the Path names.
    """

    readers = []
    for record_type in settings.record_types:
        if record_type == RecordType.WIKIPEDIA:
            readers.extend(
                [
                    WikipediaReader(output_file_path)
                    for output_file_path in settings.output_file_paths
                    if record_type in str(output_file_path)
                ]
            )

    return tuple(readers)
