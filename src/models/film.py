from typing import List, Optional

from pydantic import BaseModel, Field


class FilmPerson(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float | None = Field(None)
    title: str
    description: str | None = Field("")

    director: List[Optional[str]]
    actors_names: List[Optional[str]]
    writers_names: List[Optional[str]]

    actors: List[Optional[FilmPerson]]
    writers: List[Optional[FilmPerson]]
