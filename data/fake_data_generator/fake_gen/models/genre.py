from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Genre(TypedDict):
    id: UUID
    name: str
    description: str

    created: datetime
    modified: datetime
