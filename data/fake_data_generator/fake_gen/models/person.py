from datetime import datetime
from typing import TypedDict
from uuid import UUID


class Person(TypedDict):
    id: UUID
    full_name: str

    created: datetime
    modified: datetime
