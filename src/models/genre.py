from pydantic import BaseModel, Field


class GenreFilm(BaseModel):
    id: str
    title: str
    description: str | None = Field("")


class Genre(BaseModel):
    id: str
    name: str
