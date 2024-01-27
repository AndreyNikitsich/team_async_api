from datetime import datetime
from typing import TypedDict
from uuid import UUID


class GenreFilm(TypedDict):
    id: UUID
    genre_id: UUID
    film_id: UUID

    created: datetime
