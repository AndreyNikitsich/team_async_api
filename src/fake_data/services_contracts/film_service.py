from functools import lru_cache
from typing import Optional
from uuid import UUID

from ..fake_data import FAKE_FILMS, FAKE_PERSONS_FILMS
from ..models.film import Film, PersonsFilm


class FilmService:
    async def get_by_id(self, film_id: UUID) -> Optional[Film]:
        return FAKE_FILMS[1]

    async def get_films(
        self,
        *,
        page_size: int,
        page_number: int,
        sorting_fields: list[str] | None = None,
        genres: list[str] | None = None,
    ) -> list[Film]:
        return FAKE_FILMS

    async def get_films_for_person(self, *, person_id: UUID, page_size: int, page_number: int) -> list[PersonsFilm]:
        return FAKE_PERSONS_FILMS

    async def get_by_search(self, *, page_size: int, page_number: int, query: str) -> list[Film]:
        return FAKE_FILMS


@lru_cache()
def get_film_service() -> FilmService:
    return FilmService()
