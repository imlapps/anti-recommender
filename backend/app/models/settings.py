from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models.types import AntiRecommenderType, ApiKey, RecordType

CONFIG_DIRECTORY_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_DIRECTORY_PATH = Path(__file__).parent.parent.absolute() / "data"


class Settings(BaseSettings):
    """A Pydantic BaseSetting to hold environment variables."""

    record_types: frozenset[RecordType] = frozenset()
    output_file_paths: frozenset[Path] = Field(
        default=frozenset(), validation_alias="output_file_names"
    )
    anti_recommender_type: AntiRecommenderType = AntiRecommenderType.OPEN_AI
    wikipedia_arkg_file_path: Annotated[
        Path, Field(min_length=1, json_schema_extra={"strip_whitespace": "True"})
    ] = (DATA_DIRECTORY_PATH / "wikipedia_arkg_file.ttl")
    openai_api_key: ApiKey | None = None

    model_config = SettingsConfigDict(
        env_file=(
            CONFIG_DIRECTORY_PATH / ".env.local",
            CONFIG_DIRECTORY_PATH / ".env.secret",
        ),
        extra="ignore",
        env_file_encoding="utf-8",
        validate_default=False,
    )

    @field_validator("output_file_paths", mode="before")
    @classmethod
    def convert_to_list_of_file_paths(
        cls, output_file_names: frozenset[str]
    ) -> frozenset[Path]:
        """Convert the list of file names in the environment variables into a list of Path objects."""
        return frozenset(
            [DATA_DIRECTORY_PATH / file_name for file_name in output_file_names]
        )

    @field_validator("wikipedia_arkg_file_path", mode="before")
    @classmethod
    def convert_to_file_path(cls, wikipedia_arkg_file_name: str) -> Path:
        """Convert the file name of an ARKG into a data directory Path."""

        return DATA_DIRECTORY_PATH / wikipedia_arkg_file_name


settings = Settings()
