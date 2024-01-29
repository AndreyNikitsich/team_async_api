from typing import List

from pydantic import BaseModel


class PersonFilm(BaseModel):
    id: str
    title: str
    roles: List[str]


class Person(BaseModel):
    id: str
    full_name: str
