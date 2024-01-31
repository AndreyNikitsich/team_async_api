from functools import lru_cache
from typing import Annotated

from core.config import settings
from fastapi import Depends
from models.film import Film

from services.db import ElasticService


class FilmService:
    """Содержит бизнес-логику по работе с фильмами."""

    def __init__(self, elastic_service: ElasticService):
        self.elastic_service = elastic_service

    async def get_films(
        self, *, page_size: int, page_number: int, sort: list[str] | None = None, genre: list[str] | None = None
    ) -> list[Film]:
        """
        Возвращает список фильмов по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """
        query_match = None

        if genre is not None:
            query_match = {"terms": {"genres_names": genre, "boost": 1.0}}

        data = await self.elastic_service.search_models(
            index=settings.es.FILMS_INDEX,
            page_number=page_number,
            page_size=page_size,
            query_match=query_match,
            sort=sort,
        )

        if not data:
            return []

        films = [Film(**row["_source"]) for row in data]

        return films

    async def get_by_search(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: list[str] | None = None,
    ) -> list[Film]:
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
                        "genres_names",
                        "directors_names",
                    ],
                }
            }

        data = await self.elastic_service.search_models(
            index=settings.es.FILMS_INDEX,
            page_number=page_number,
            page_size=page_size,
            query_match=query_match,
            sort=sort,
        )

        if not data:
            return []

        films = [Film(**row["_source"]) for row in data]

        return films

    async def get_by_id(self, film_id: str) -> Film | None:
        """
        Возвращает объект фильма по id (uuid).
        Он опционален, так как фильм может отсутствовать в базе.
        """
        data = await self.elastic_service.get_model(index=settings.es.FILMS_INDEX, model_id=film_id)
        if not data:
            return None

        return Film(**data)


@lru_cache()
def get_film_service(
    db_service: Annotated[ElasticService, Depends()],
) -> FilmService:
    """Провайдер FilmService."""
    return FilmService(db_service)
