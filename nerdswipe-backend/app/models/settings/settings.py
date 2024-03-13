
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    model_confg = SettingsConfigDict(
        env_file=(Path(__file__).parent.parent.parent.parent / '.local.env',
                  Path(__file__).parent.parent.parent.parent / '.env.secret'),
        extra='ignore'
    )

    record_types: frozenset[str] | None = None
    output_file_names: frozenset[str] | None = None
    anti_recommender_type: str = "OpenAI"
    openai_api_key: str | None = None


settings = __Settings()
