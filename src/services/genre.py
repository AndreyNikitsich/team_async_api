from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from core.config import settings
from models.genre import Genre
from services.db import ElasticService


class GenreService:
    """Содержит бизнес-логику по работе с жанрами."""

    def __init__(self, elastic_service: ElasticService):
        self.elastic_service = elastic_service

    async def get_genres(
        self,
        *,
        page_size: int,
        page_number: int,
        sort: list[str] | None = None,
    ) -> list[Genre]:
        """
        Возвращает список жанров по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """
        data = await self.elastic_service.search_models(
            index=settings.es.GENRE_INDEX, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        genres = [Genre(**row["_source"]) for row in data]

        return genres

    async def get_by_search(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: list[str] | None = None,
    ) -> list[Genre]:
        """
        Возвращает список жанров по поиску.
        Может возвращать пустой список, так как по запросу могут
        отсутствовать жанры в базе.
        """
        query_match = None

        if query is not None:
            query_match = {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": [
                        "name",
                        "descriptions",
                    ],
                }
            }

        data = await self.elastic_service.search_models(
            index=settings.es.GENRE_INDEX, query=query_match, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        genres = [Genre(**row["_source"]) for row in data]

        return genres

    async def get_by_id(self, genre_id: str) -> Genre | None:
        """
        Возвращает объект жанра по id (uuid).
        Он опционален, так как жанр может отсутствовать в базе.
        """
        data = await self.elastic_service.get_model(index=settings.es.GENRE_INDEX, model_id=genre_id)
        if not data:
            return None

        return Genre(**data)


@lru_cache()
def get_genre_service(
    db_service: Annotated[ElasticService, Depends()],
) -> GenreService:
    return GenreService(db_service)
