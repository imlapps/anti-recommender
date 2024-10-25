from pathlib import Path

from pydantic import AnyUrl, Field, FilePath, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyoxigraph import NamedNode

from app.models.types import AntiRecommenderType, RdfMimeType, RecordType

CONFIG_DIRECTORY_PATH = Path(__file__).parent.parent.parent.absolute()
DATA_DIRECTORY_PATH = Path(__file__).parent.parent.absolute() / "data"


class Settings(BaseSettings):
    """Pydantic BaseSettings to hold environment variables."""

    arkg_base_iri: NamedNode = NamedNode(
        "http://imlapps.github.io/anti-recommender/anti-recommendation/"
    )
    arkg_file_path: FilePath = DATA_DIRECTORY_PATH / "wikipedia_arkg_file.ttl"
    arkg_mime_type: RdfMimeType = RdfMimeType.TURTLE

    anti_recommender_type: AntiRecommenderType = AntiRecommenderType.ARKG
    openai_api_key: SecretStr | None = None
    output_file_paths: frozenset[Path] = Field(
        default=frozenset(), validation_alias="output_file_names"
    )
    record_types: frozenset[RecordType] = frozenset()
    supabase_url: AnyUrl | None = None
    supabase_key: SecretStr | None = None
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
        """Convert the list of file names in the environment variables into a list of Paths."""

        return frozenset(
            [DATA_DIRECTORY_PATH / file_name for file_name in output_file_names]
        )

    @field_validator("arkg_file_path", mode="before")
    @classmethod
    def convert_to_file_path(cls, arkg_file_name: str) -> Path:
        """Convert the file name of an ARKG into a Path."""

        return DATA_DIRECTORY_PATH / arkg_file_name
