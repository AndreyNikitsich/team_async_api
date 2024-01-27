from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Definition(TypedDict):
    id: UUID
    name: str

    created: datetime
    modified: datetime
