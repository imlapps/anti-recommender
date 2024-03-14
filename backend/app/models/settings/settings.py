from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):  # noqa: N801

    record_types: frozenset[str] | None = None
    output_file_names: frozenset[str] | None = None
    anti_recommender_type: str = "OpenAI"
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).parent.parent.parent.parent / ".env.local",
            Path(__file__).parent.parent.parent.parent / ".env.secret",
        ),
        extra="ignore",
        env_file_encoding="utf-8",
    )


settings = __Settings()
