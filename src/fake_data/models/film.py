from typing import List
from uuid import UUID

from pydantic import BaseModel


class FilmPerson(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: UUID
    imdb_rating: float | None = None
    title: str = ""
    description: str = ""

    director: List[FilmPerson] = []
    # actors_names: List[str]  noqa: ERA001
    # writers_names: List[str]  noqa: ERA001

    actors: List[FilmPerson] = []
    writers: List[FilmPerson] = []


class PersonsFilm(BaseModel):
    id: UUID
    imdb_rating: float | None = None
    title: str = ""
    roles: list[str] = []
