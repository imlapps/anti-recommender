from pathlib import Path

__all__ = ["wikipedia_output_path"]

# The file path for the Wikipedia abstracts output data.
wikipedia_output_path = Path(__file__).parent / "mini-wikipedia.output.txt"
