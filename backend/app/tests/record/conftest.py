import pytest
from app.record.wikipedia_record.wikipedia_record import WikipediaRecord


@pytest.fixture(scope="module")
def wikipedia_records():
    """This fixture returns a dictionary containing sample Wikipedia records."""

    return tuple([{
        "test-wikipedia-article-1": {
            "test-info": "test info for test-wikipedia-article-1"
        },
    }])


@pytest.fixture(scope="module")
def wikipedia_record(wikipedia_records):
    """
    This fixture yields a WikipediaRecord object.
    """

    yield WikipediaRecord(wikipedia_records)


@pytest.fixture(scope="module")
def first_wikipedia_record_item(wikipedia_records):
    """
    This fixture returns a tuple of the first item in wikipedia_records
    """

    return tuple([{list(wikipedia_records[0].keys())[0]:
                   wikipedia_records[0][list(wikipedia_records[0].keys())[0]]
                   }]
                 )
