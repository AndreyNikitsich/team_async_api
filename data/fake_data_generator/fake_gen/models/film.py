from datetime import datetime
from typing import TypedDict
from uuid import UUID

from .accessibility import Accessibility
from .mpaa_rating import MPAARating


class Film(TypedDict):
    id: UUID
    title: str
    imdb_rating: float
    mpaa_rating: MPAARating
    accessibility_features: list[Accessibility]
    duration_settings: int
    release_date: datetime
    description: str

    created: datetime
    modified: datetime
