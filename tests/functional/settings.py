import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.config import BASE_DIR


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8", extra="ignore"
    )


class ElasticSettings(EnvSettings):
    ES_SCHEMA: str = Field(default="http")
    ES_HOST: str = Field(default="127.0.0.1")
    ES_PORT: int = Field(default=9200)
    FILMS_INDEX: str = Field(default="movies")
    PERSONS_INDEX: str = Field(default="persons")
    GENRE_INDEX: str = Field(default="genres")

class RedisSettings(EnvSettings):
    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)


class TestSettings(EnvSettings):
    redis: RedisSettings = RedisSettings()
    es: ElasticSettings = ElasticSettings()


test_settings = TestSettings()