from functools import lru_cache
from typing import Annotated, List, Optional

from core.config import settings
from fastapi import Depends
from models.genre import Genre

from services.cache import CacheService
from services.db import ElasticService


class GenreService:
    """Содержит бизнес-логику по работе с жанрами."""

    def __init__(self, cache_service: CacheService, elastic_service: ElasticService):
        self.cache_service = cache_service
        self.elastic_service = elastic_service

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """
        Возвращает объект жанра по id (uuid).
        Он опционален, так как жанр может отсутствовать в базе.
        """
        genre = await self.cache_service.get_model_cache(genre_id, Genre)
        if not genre:
            genre = await self.elastic_service.get_model(
                model=Genre,
                index=settings.es.GENRE_INDEX,
                id_=genre_id,
            )
            if not genre:
                return None
            await self.cache_service.put_model_cache(genre_id, genre)

        return genre

    async def get_genres(
            self, *,
            page_size: int,
            page_number: int,
            sort: Optional[List[str]] = None,
    ) -> List[Genre]:
        """
        Возвращает список жанров по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """
        genres = await self.elastic_service.search_models(
            model=Genre,
            index=settings.es.GENRE_INDEX,
            sort=sort,
            page_size=page_size,
            page_number=page_number,
        )

        return genres

    async def get_by_search(
            self, *,
            page_size: int,
            page_number: int,
            query: str,
            sort: Optional[List[str]] = None,
    ) -> List[Genre]:
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
                        "films_titles",
                        "films_descriptions",
                    ]
                }
            }

        genres = await self.elastic_service.search_models(
            model=Genre,
            index=settings.es.GENRE_INDEX,
            sort=sort,
            page_size=page_size,
            page_number=page_number,
            query=query_match
        )

        return genres


@lru_cache()
def get_genre_service(
        cache_service: Annotated[CacheService, Depends()],
        db_service: Annotated[ElasticService, Depends()],
) -> GenreService:
    return GenreService(cache_service, db_service)
