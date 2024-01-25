import os 
from app.utils.json import json_loader

def test_successfully_load_data() -> None:
    """
    Test to check that the json_loader correctly reads in the Wikipedia output data.
    """

    file_path = os.getcwd()+"\\app\\tests\\data\\test-mini-wikipedia.output.txt"
    wikipedia_data = json_loader.load_data(file_path)[0]

    assert list(wikipedia_data.keys())[0] == "Amphibian"


def test_unsuccessfully_load_data_with_incorrect_file_path() -> None:
    """
    Test to check that the json_loader does not read in any data when an incorrect file path is given.
    """

    pass 

def test_unsuccessfully_load_data_with_invalid_JSON_format() -> None:
    """
    Test to check that the json_loader returns an Exception when the input file contains an incorrect JSON format.
    """
        
    pass