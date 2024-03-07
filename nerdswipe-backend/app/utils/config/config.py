import os
from pathlib import Path
from dotenv import dotenv_values

config = (
    {
        # load shared development variables
        **dotenv_values(Path(__file__).parent.parent.parent.parent / ".env.local"),
        # load sensitive variables
        **dotenv_values(Path(__file__).parent.parent.parent.parent / ".env.secret"),
        **os.environ,  # override loaded values with environment variables
    },
)
