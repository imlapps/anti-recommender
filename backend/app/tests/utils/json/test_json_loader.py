from app.utils.json import json_loader
from app.data.wikipedia_output_path import wikipedia_output_path

import pytest
import json


@pytest.mark.parametrize(
    "test_input,expected", [(wikipedia_output_path, tuple), ("", int)]
)
def test_load_json_data(test_input, expected):

    assert type(json_loader.load_data(test_input)) == expected


def test_raises_exception_when_parsing_json_data(mocker):
    mocker.patch.object(json, "loads", return_value=json.JSONDecodeError)

    with pytest.raises(Exception):
        json_loader.load_data(wikipedia_output_path)
