
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):

    record_types: frozenset[str]
    output_file_names: frozenset[str]
    anti_recommender_type: str = "OpenAI"
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=(Path(__file__).parent.parent.parent.parent / '.env.local',
                  Path(__file__).parent.parent.parent.parent / '.env.secret'),
        extra='ignore',
        env_file_encoding="utf-8"
    )


settings = __Settings()
