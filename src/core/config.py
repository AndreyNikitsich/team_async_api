import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8", extra="ignore"
    )


class ProjectMetadataSettings(EnvSettings):
    PROJECT_NAME: str = Field(default="movies")
    DOCS_URL: str = "/api/openapi"
    OPENAPI_URL: str = "/api/openapi.json"
    VERSION: str = "0.1.0"


class RedisSettings(EnvSettings):
    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)
    CACHE_EXPIRE_IN_SECONDS: int = Field(default=(60 * 5))


class ElasticSettings(EnvSettings):
    ES_SCHEMA: str = Field(default="http")
    ES_HOST: str = Field(default="127.0.0.1")
    ES_PORT: int = Field(default=9200)
    FILMS_INDEX: str = Field(default="movies")
    PERSONS_INDEX: str = Field(default="persons")
    GENRE_INDEX: str = Field(default="genres")


class ApiSettings(EnvSettings):
    DEFAULT_PAGE_NUMBER: int = 1
    DEFAULT_PAGE_SIZE: int = 50


class Settings(BaseSettings):
    project_metadata: ProjectMetadataSettings = ProjectMetadataSettings()
    redis: RedisSettings = RedisSettings()
    es: ElasticSettings = ElasticSettings()
    api: ApiSettings = ApiSettings()


settings = Settings()
