from functools import lru_cache
from typing import Optional
from uuid import UUID

from ..fake_data import FAKE_PERSONS
from ..models.person import Person


class PersonService:
    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        return FAKE_PERSONS[3]

    async def get_by_search(self, *, query: str, page_size: int, page_number: int) -> list[Person]:
        return FAKE_PERSONS


@lru_cache()
def get_person_service() -> PersonService:
    return PersonService()
