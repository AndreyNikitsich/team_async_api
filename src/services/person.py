from functools import lru_cache
from typing import Annotated

from core.config import settings
from fastapi import Depends
from models.person import Person, PersonFilm

from services.db import ElasticService


class PersonService:
    """Содержит бизнес-логику по работе с персонами."""

    def __init__(self, elastic_service: ElasticService):
        self.elastic_service = elastic_service

    async def get_by_id(self, person_id: str) -> Person | None:
        """
        Возвращает объект персоны по id (uuid).
        Он опционален, так как персона может отсутствовать в базе.
        """
        data = await self.elastic_service.get_model(index=settings.es.PERSONS_INDEX, model_id=person_id)
        if not data:
            return None

        return Person(**data)

    async def get_films_for_person(
            self, *,
            person_id: str,
            page_size: int,
            page_number: int,
            sort: list[str] | None = None,
    ) -> list[PersonFilm]:
        """
        Возвращает список фильмов у персоны.
        """
        query_match = {
            "bool": {
                "must": {
                    "term": {"id": person_id}
                },
                "filter": {
                    "nested": {
                        "path": "films",
                        "query": {
                            "match_all": {}
                        },
                        "inner_hits": {
                            "size": page_size,
                            "from": page_number
                        }
                    }
                }
            }
        }

        data = await self.elastic_service.search_models(
            index=settings.es.PERSONS_INDEX,
            query=query_match,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
            inner_hits=True
        )

        if not data:
            return []

        data_films = [row["inner_hits"]["films"]["hits"]["hits"] for row in data]

        if not data_films:
            return []

        films = [PersonFilm(**row["_source"]) for row in data_films]

        return films

    async def get_persons(
        self,
        *,
        page_size: int,
        page_number: int,
        sort: list[str] | None = None,
    ) -> list[Person]:
        """
        Возвращает список персон по параметрам.
        Может возвращать пустой список, так как база фильмов может быть пуста.
        """
        data = await self.elastic_service.search_models(
            index=settings.es.PERSONS_INDEX, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        return [Person(**row["_source"]) for row in data]

    async def get_by_search(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: list[str] | None = None,
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
                        "full_name",
                    ],
                }
            }

        data = await self.elastic_service.search_models(
            index=settings.es.PERSONS_INDEX, query=query_match, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        persons = [Person(**row["_source"]) for row in data]

        return persons


@lru_cache()
def get_person_service(
    db_service: Annotated[ElasticService, Depends()],
) -> PersonService:
    return PersonService(db_service)
