from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PersonBase(BaseModel):
    uuid: UUID
    full_name: str


class PersonInfo(PersonBase):
    # may add some extra info
    pass


class GenreBase(BaseModel):
    uuid: UUID
    name: str


class GenreInfo(GenreBase):
    # may add description, etc.
    pass


class FilmBase(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: Optional[float]


class PersonsFilm(FilmBase):
    roles: list[str]


class FilmInfo(FilmBase):
    description: str
    genre: list[GenreBase]
    actors: list[PersonBase]
    writers: list[PersonBase]
    directors: list[PersonBase]
