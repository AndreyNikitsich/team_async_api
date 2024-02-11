from pydantic import BaseModel, ConfigDict, Field


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

    genres: list[FilmGenres]
    genres_names: list[str]

    directors: list[FilmPerson]
    directors_names: list[str]

    actors: list[FilmPerson]
    actors_names: list[str]

    writers: list[FilmPerson]
    writers_names: list[str]

    model_config = ConfigDict(extra="ignore")
