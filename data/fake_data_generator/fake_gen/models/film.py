from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Film(TypedDict):
    id: UUID
    title: str
    imdb_rating: float
    release_date: datetime
    description: str

    created: datetime
    modified: datetime
