from functools import lru_cache
from typing import Annotated, List, Optional

from core.config import settings
from fastapi import Depends
from models.film import Film

from services.cache import CacheService
from services.db import ElasticService


class FilmService:
    """Содержит бизнес-логику по работе с фильмами."""

    def __init__(
            self,
            cache_service: CacheService,
            elastic_service: ElasticService
    ):
        self.cache_service = cache_service
        self.elastic_service = elastic_service

    async def get_films(
            self, *,
            page_size: int,
            page_number: int,
            sort: Optional[List[str]] = None,
            genre: Optional[List[str]] = None
    ) -> List[Film]:
        """
        Возвращает список фильмов по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """
        query_match = None

        if genre is not None:
            query_match = {
                "terms": {
                    "genre": genre,
                    "boost": 1.0
                }
            }

        films = await self.elastic_service.search_models(
            model=Film,
            index=settings.es.FILMS_INDEX,
            sort=sort,
            page_size=page_size,
            page_number=page_number,
            query=query_match
        )

        return films

    async def get_by_search(
            self, *,
            page_size: int,
            page_number: int,
            query: str,
            sort: Optional[List[str]] = None,
    ) -> List[Film]:
        """
        Возвращает список фильмов по поиску.
        Может возвращать пустой список, так как по запросу могут
        отсутствовать фильмы в базе.
        """
        query_match = None

        if query is not None:
            query_match = {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": [
                        "actors_names",
                        "writers_names",
                        "title",
                        "description",
                        "genre",
                        "director"
                    ]
                }
            }

        films = await self.elastic_service.search_models(
            model=Film,
            index=settings.es.FILMS_INDEX,
            sort=sort,
            page_size=page_size,
            page_number=page_number,
            query=query_match
        )

        return films

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        """
        Возвращает объект фильма по id (uuid).
        Он опционален, так как фильм может отсутствовать в базе.
        """
        film = await self.cache_service.get_model_cache(film_id, Film)
        if not film:
            film = await self.elastic_service.get_model(
                model=Film,
                index=settings.es.FILMS_INDEX,
                id_=film_id,
            )
            if not film:
                return None
            await self.cache_service.put_model_cache(film_id, film)

        return film


@lru_cache()
def get_film_service(
        cache_service: Annotated[CacheService, Depends()],
        db_service: Annotated[ElasticService, Depends()],
) -> FilmService:
    """Провайдер FilmService."""
    return FilmService(cache_service, db_service)
