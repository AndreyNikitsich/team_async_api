from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Cover(TypedDict):
    id: UUID
    film_id: UUID
    size: str
    url: str

    created: datetime
    modified: datetime
