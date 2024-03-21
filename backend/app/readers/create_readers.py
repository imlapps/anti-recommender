from app.models.settings import BaseSettings
from app.readers.reader.reader import Reader
from app.readers.reader.wikipedia_reader import WikipediaReader


def create_readers(settings) -> tuple[Reader | None, ...]:
    """
    Return a tuple of Readers depending on the record type obtained from settings.
    Readers are instantiated with Paths that contain the corresponding record types in the Path names.
    """

    readers = []
    for record_type in settings.record_types:
        if record_type.lower() == "wikipedia":

            readers.extend(
                [
                    WikipediaReader(output_file_path)
                    for output_file_path in settings.output_file_paths
                    if record_type.lower() in str(output_file_path)
                ]
            )

    return tuple(readers)
