from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from testdata import es_mapping


class TestSettings(BaseSettings):
    es_url: str = Field("http://127.0.0.1:9200")
    es_index: str = Field("movies")
    es_id_field: str = Field("id")
    es_index_mapping: dict[str, Any] = Field(es_mapping.MOVIES_MAPPING)

    redis_host: str = Field("localhost")
    redis_port: int = Field(6379)

    service_url: str = Field("http://127.0.0.1:8000")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore")


class FilmSettings(TestSettings):
    es_index: str = Field("movies")
    es_index_mapping: dict[str, Any] = Field(es_mapping.MOVIES_MAPPING)


class GenreSettings(TestSettings):
    es_index: str = Field("genres")
    es_index_mapping: dict[str, Any] = Field(es_mapping.GENRES_MAPPING)


class PersonSettings(TestSettings):
    es_index: str = Field("persons")
    es_index_mapping: dict[str, Any] = Field(es_mapping.PERSONS_MAPPING)


test_settings = TestSettings()
film_settings = FilmSettings()
genre_settings = GenreSettings()
person_settings = PersonSettings()
