from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.models.types import AntiRecommenderType, RecordType


CONFIG_FILE_PATH = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """A Pydantic BaseSetting to hold environment variables."""

    record_types: frozenset[RecordType] = frozenset()
    output_file_paths: frozenset[Path] = Field(
        default=frozenset(), validation_alias="output_file_names"
    )
    anti_recommender_type: AntiRecommenderType = AntiRecommenderType.OPEN_AI
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=(
            CONFIG_FILE_PATH / ".env.local",
            CONFIG_FILE_PATH / ".env.secret",
        ),
        extra="ignore",
        env_file_encoding="utf-8",
        validate_default=False,
    )

    @field_validator("output_file_paths", mode="before")
    @classmethod
    def convert_to_list_of_file_paths(cls, output_file_names: list[str]) -> frozenset[Path]:
        """Convert the list of file names in the environment variables into a list of Path objects."""
        return [
            Path(__file__).parent.parent / "data" / file_name
            for file_name in output_file_names
        ]


settings = Settings()
