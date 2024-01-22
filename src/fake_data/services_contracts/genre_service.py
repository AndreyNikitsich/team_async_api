from functools import lru_cache
from typing import Optional
from uuid import UUID

from ..fake_data import FAKE_GENRES
from ..models.genre import Genre


class GenreService:
    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        return FAKE_GENRES[0]

    async def get_genres(self) -> list[Genre]:
        return FAKE_GENRES


@lru_cache()
def get_genre_service() -> GenreService:
    return GenreService()
