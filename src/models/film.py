from typing import List

from pydantic import BaseModel, Field


class FilmGenres(BaseModel):
    id: str
    name: str


class FilmPerson(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float | None = Field(None)
    title: str
    description: str | None = Field("")

    genres: List[FilmGenres]
    genres_names: List[str]

    directors: List[FilmPerson]
    directors_names: List[str]

    actors: List[FilmPerson]
    actors_names: List[str]

    writers: List[FilmPerson]
    writers_names: List[str]
