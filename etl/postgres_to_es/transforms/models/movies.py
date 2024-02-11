from pydantic import BaseModel, Field


class ESPerson(BaseModel):
    """Модель данных персон для индексации в Elasticsearch."""

    id: str = Field(..., validation_alias="person_id")
    name: str = Field(..., validation_alias="person_name")


class ESMovie(BaseModel):
    """Модель данных фильмов для индексации в Elasticsearch."""

    id: str
    rating: float | None = Field(None, serialization_alias="imdb_rating")
    title: str
    description: str | None = None

    genres: list[str] | None = Field(
        [], serialization_alias="genre")

    director_names: list[str] | None = Field(
        [], serialization_alias="director")
    actor_names: list[str] | None = Field(
        [], serialization_alias="actors_names")
    writer_names: list[str] | None = Field(
        [], serialization_alias="writers_names")

    actor: list[ESPerson] | None = Field(
        [], serialization_alias="actors")
    writer: list[ESPerson] | None = Field(
        [], serialization_alias="writers")
