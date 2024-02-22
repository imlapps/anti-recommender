
def test_get_wikipedia_record(wikipedia_record, first_wikipedia_record_item):
    """Test that WikipediaRecord stores and returns a record from storage."""

    assert wikipedia_record.get_record(
        "test-wikipedia-article-1") == first_wikipedia_record_item


def test_get_wikipedia_record_returns_none(wikipedia_record):
    """Test that WikipediaRecord returns None when a given article does not exist in storage."""

    assert wikipedia_record.get_record("random-wikipedia-article") == None
