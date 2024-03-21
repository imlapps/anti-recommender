from pathlib import Path
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field

config_parent_path = Path(__file__).parent.parent.parent.parent


class AntiRecommenderType(str, Enum):
    """An enum of anti-recommender types."""

    open_ai = "OpenAI"


class RecordType(str, Enum):
    """An enum of record types."""

    wikipedia = "Wikipedia"


class __Settings(BaseSettings):  # noqa: N801
    """A Pydantic BaseSetting to hold environment variables."""

    record_types: frozenset[RecordType] | None = None
    output_file_paths: frozenset[Path] | None = Field(
        validation_alias="output_file_names")
    anti_recommender_type: AntiRecommenderType = AntiRecommenderType.open_ai
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=(
            config_parent_path / ".env.local",
            config_parent_path / ".env.secret",
        ),
        extra="ignore",
        env_file_encoding="utf-8",
        validate_default=False
    )

    @field_validator("output_file_paths", mode="before")
    @classmethod
    def convert_to_list_of_file_paths(cls, output_file_names: list[str]) -> list[Path]:
        """Convert the list of file names in the environment variables into a list of Path objects."""
        return [
            Path(__file__).parent.parent.parent / "data" / file_name
            for file_name in output_file_names
        ]


settings = __Settings(output_file_paths=None)
