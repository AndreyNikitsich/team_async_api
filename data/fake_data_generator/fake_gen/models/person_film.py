from datetime import datetime
from typing import TypedDict
from uuid import UUID

from .roles import Roles


class PersonFilm(TypedDict):
    id: UUID
    person_id: UUID
    film_id: UUID
    role: Roles

    created: datetime
    modified: datetime
