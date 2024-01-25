from functools import lru_cache
from typing import Annotated, List, Optional

from core.config import settings
from fastapi import Depends
from models.person import Person

from services.cache import CacheService
from services.db import ElasticService


class PersonService:
    """Содержит бизнес-логику по работе с персонами."""

    def __init__(self, cache_service: CacheService, elastic_service: ElasticService):
        self.cache_service = cache_service
        self.elastic_service = elastic_service

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        """
        Возвращает объект персоны по id (uuid).
        Он опционален, так как персона может отсутствовать в базе.
        """
        person = await self.cache_service.get_model_cache(person_id, Person)
        if not person:
            person = await self.elastic_service.get_model(
                model=Person,
                index=settings.es.PERSONS_INDEX,
                id_=person_id,
            )
            if not person:
                return None
            await self.cache_service.put_model_cache(person_id, person)

        return person

    async def get_persons(
            self, *,
            page_size: int,
            page_number: int,
            sort: Optional[List[str]] = None,
    ) -> List[Person]:
        """
        Возвращает список персон по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """
        persons = await self.elastic_service.search_models(
            model=Person,
            index=settings.es.PERSONS_INDEX,
            sort=sort,
            page_size=page_size,
            page_number=page_number,
        )

        return persons

    async def get_by_search(
            self, *,
            page_size: int,
            page_number: int,
            query: str,
            sort: Optional[List[str]] = None,
    ) -> list[Person]:
        """
        Возвращает список персон по поиску.
        Может возвращать пустой список, так как по запросу могут
        отсутствовать персоны в базе.
        """
        query_match = None

        if query is not None:
            query_match = {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": [
                        "name",
                        "roles",
                        "films_titles",
                        "films_descriptions",
                    ]
                }
            }

        persons = await self.elastic_service.search_models(
            model=Person,
            index=settings.es.PERSONS_INDEX,
            sort=sort,
            page_size=page_size,
            page_number=page_number,
            query=query_match
        )

        return persons


@lru_cache()
def get_person_service(
        cache_service: Annotated[CacheService, Depends()],
        db_service: Annotated[ElasticService, Depends()],
) -> PersonService:
    return PersonService(cache_service, db_service)
