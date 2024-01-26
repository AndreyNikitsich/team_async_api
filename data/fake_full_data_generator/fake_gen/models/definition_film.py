from datetime import datetime
from typing import TypedDict
from uuid import UUID


class DefinitionFilm(TypedDict):
    id: UUID
    definition_id: UUID
    film_id: UUID

    created: datetime
