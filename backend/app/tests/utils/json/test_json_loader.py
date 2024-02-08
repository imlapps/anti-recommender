from app.utils.json import json_loader
from app.data.wikipedia_output_path import wikipedia_output_path

import pytest
import json


@pytest.mark.parametrize(
    "test_file_path,expected_output", [(wikipedia_output_path, tuple), ("", int)]
)
def test_load_json_data(test_file_path, expected_output):
    """Test that the json_loader's output matches the expected output, for a given file path."""
    assert type(json_loader.load_data(test_file_path)) == expected_output


def test_raises_exception_when_parsing_json_data(mocker):
    """Test that the json_loader raises an Exception when it encounters a JSONDecodeError."""

    # Mock json.loads() and return a JSONDecodeError
    mocker.patch.object(json, "loads", return_value=json.JSONDecodeError)

    with pytest.raises(Exception):
        json_loader.load_data(wikipedia_output_path)
