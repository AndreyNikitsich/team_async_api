from pydantic import BaseModel


class BasePersonResponse(BaseModel):
    uuid: str
    full_name: str


class DetailPersonResponse(BasePersonResponse):
    pass


class BaseGenreResponse(BaseModel):
    uuid: str
    name: str


class DetailGenreResponse(BaseGenreResponse):
    pass


class BaseFilmResponse(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None


class PersonsFilmResponse(BaseFilmResponse):
    roles: list[str]


class DetailFilmResponse(BaseFilmResponse):
    description: str
    genres: list[BaseGenreResponse]
    actors: list[BasePersonResponse]
    writers: list[BasePersonResponse]
    directors: list[BasePersonResponse]
