from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from testdata import es_mapping


class TestSettings(BaseSettings):
    ES_URL: str = Field("http://127.0.0.1:9200")
    ES_INDEX: str = Field("movies")
    ES_ID_FIELD: str = Field("id")
    ES_INDEX_MAPPING: dict[str, Any] = Field(es_mapping.MOVIES_MAPPING)

    REDIS_HOST: str = Field("localhost")
    REDIS_PORT: int = Field(6379)

    SERVICE_URL: str = Field("http://127.0.0.1:8000")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore")


class FilmSettings(TestSettings):
    ES_INDEX: str = Field("movies")
    ES_INDEX_MAPPING: dict[str, Any] = Field(es_mapping.MOVIES_MAPPING)


class GenreSettings(TestSettings):
    ES_INDEX: str = Field("genres")
    ES_INDEX_MAPPING: dict[str, Any] = Field(es_mapping.GENRES_MAPPING)


class PersonSettings(TestSettings):
    ES_INDEX: str = Field("persons")
    ES_INDEX_MAPPING: dict[str, Any] = Field(es_mapping.PERSONS_MAPPING)


test_settings = TestSettings()
film_settings = FilmSettings()
genre_settings = GenreSettings()
person_settings = PersonSettings()
