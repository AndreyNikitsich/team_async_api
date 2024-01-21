import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmPerson(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float | None = Field(None)
    title: str
    description: str | None = Field("")

    director: list[str] | None = Field([])
    actors_names: list[str] | None = Field([])
    writers_names: list[str] | None = Field([])

    actors: list[FilmPerson] | None = Field([])
    writers: list[FilmPerson] | None = Field([])

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
