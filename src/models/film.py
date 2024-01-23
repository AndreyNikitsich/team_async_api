from typing import List

from pydantic import BaseModel, Field


class FilmPerson(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float | None = Field(None)
    title: str
    description: str | None = Field("")

    director: List[str]
    actors_names: List[str]
    writers_names: List[str]

    actors: List[FilmPerson]
    writers: List[FilmPerson]
