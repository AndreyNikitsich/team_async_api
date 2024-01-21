from functools import lru_cache
from typing import List, Optional

from core import config
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film
from redis.asyncio import Redis


class FilmService:
    """Содержит бизнес-логику по работе с фильмами."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_films(self, *, sort=None,
                        page_size=50, page_number=1) -> List[Optional[Film]]:
        """
        Возвращает список фильмов по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """

    async def _get_films_from_elastic(self, sort, page_size, page_number):
        """Получаем список фильмов из Elasticsearch"""
        try:
            docs = await self.elastic.search(
                index="movies",
                sort=sort,
                size=page_size,
                from_=((page_number - 1) * page_size)
            )
        except NotFoundError:
            return None

        films = []
        for doc in docs["hits"]["hits"]:
            films.append(Film(**doc["_source"]))
        return films

    async def get_by_search(self) -> List[Optional[Film]]:
        """
        Возвращает список фильмов по поиску.
        Может возвращать пустой список, так как по этим параметрам могут
        отсутствовать фильмы в базе.
        """

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        """
        Возвращает объект фильма по id (uuid).
        Он опционален, так как фильм может отсутствовать в базе.
        """
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        """Получаем данные о фильме из Elasticsearch."""
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None

        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        """Получаем данные о фильме из кеша."""
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.model_validate(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        """Сохраняем данные о фильме в кеше."""
        await self.redis.set(film.id, film.model_dump_json(),
                             config.RedisSettings.CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    """Провайдер FilmService."""
    return FilmService(redis, elastic)
