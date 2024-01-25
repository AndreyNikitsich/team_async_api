from typing import List

from pydantic import BaseModel, Field


class PersonFilm(BaseModel):
    id: str
    title: str
    description: str | None = Field("")


class Person(BaseModel):
    id: str
    name: str
    roles: List[str]
