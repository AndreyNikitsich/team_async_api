import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8", extra="ignore"
    )


class ProjectMetadataSettings(EnvSettings):
    project_name: str = Field(default="movies")
    docs_url: str = "/api/openapi"
    openapi_url: str = "/api/openapi.json"
    version: str = "0.1.0"


class RedisSettings(EnvSettings):
    redis_host: str = Field(default="127.0.0.1")
    redis_port: int = Field(default=6379)
    cache_expire_in_seconds: int = Field(default=(60 * 5))


class ElasticSettings(EnvSettings):
    es_schema: str = Field(default="http")
    es_host: str = Field(default="127.0.0.1")
    es_port: int = Field(default=9200)
    films_index: str = Field(default="movies")
    persons_index: str = Field(default="persons")
    genre_index: str = Field(default="genres")


class ApiSettings(EnvSettings):
    default_page_number: int = 1
    default_page_size: int = 50


class Settings(BaseSettings):
    project_metadata: ProjectMetadataSettings = ProjectMetadataSettings()
    redis: RedisSettings = RedisSettings()
    es: ElasticSettings = ElasticSettings()
    api: ApiSettings = ApiSettings()
    logging_level: str = Field(default="INFO")


settings = Settings()

from logging import config as logging_config  # noqa: E402

from .logger import LOGGING  # noqa: E402

logging_config.dictConfig(LOGGING)
