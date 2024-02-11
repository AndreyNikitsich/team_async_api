from pydantic import BaseModel


class PersonFilm(BaseModel):
    id: str
    title: str
    roles: list[str]


class Person(BaseModel):
    id: str
    full_name: str
