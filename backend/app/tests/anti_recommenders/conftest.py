import os

import pytest


@pytest.fixture(autouse=True, scope="module")
def _skip_if_ci() -> None:
    """Skip if tests are run in a CI environment."""

    if "CI" in os.environ:
        pytest.skip(reason="don't have OpenAI key in CI")
