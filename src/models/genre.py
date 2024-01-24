from pydantic import BaseModel, Field


class GenreFilm(BaseModel):
    id: int
    title: str
    description: str | None = Field("")


class Genre(BaseModel):
    id: int
    name: str
