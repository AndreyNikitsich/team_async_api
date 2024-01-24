import os
from logging import config as logging_config

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8", extra="ignore"
    )


class SwaggerSettings(EnvSettings):
    PROJECT_NAME: str = Field(default="movies")
    DOCS_URL: str = "/api/openapi"
    OPENAPI_URL: str = "/api/openapi.json"


class RedisSettings(EnvSettings):
    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)
    CACHE_EXPIRE_IN_SECONDS: int = Field(default=(60 * 5))


class ElasticSettings(EnvSettings):
    ES_DSN: HttpUrl = Field(default="http://127.0.0.1:9200")
    FILMS_INDEX: str = Field(default="movies")


class ApiSettings(EnvSettings):
    DEFAULT_PAGE_NUMBER: int = 1
    DEFAULT_PAGE_SIZE: int = 50


class Settings(BaseSettings):
    swagger: SwaggerSettings = SwaggerSettings()
    redis: RedisSettings = RedisSettings()
    es: ElasticSettings = ElasticSettings()
    api: ApiSettings = ApiSettings()


settings = Settings()
