from typing import Annotated, Any

from elasticsearch import AsyncElasticsearch, BadRequestError, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from services import exceptions
from services.cache import ModelCache, QueryCache


class ElasticService:
    """Содержит бизнес-логику по работе с Elasticsearch."""

    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]):
        self.elastic = elastic

    @ModelCache(key="model_id")
    async def get_model(
            self, *,
            index: str,
            model_id: str
    ) -> dict[str, Any] | None:
        return await self._get_model(
            index=index,
            id_=model_id,
        )

    @QueryCache()
    async def search_models(
            self, *,
            index: str,
            page_number: int,
            page_size: int,
            query_match: dict[str, Any] | None,
            sort: list[str] | None
    ) -> list[dict[str, Any]] | None:
        return await self._search_models(
            index=index,
            query=query_match,
            page_number=page_number,
            page_size=page_size,
            sort=sort
        )

    async def _search_models(
            self,
            index: str,
            query: dict[str, Any] | None = None,
            page_number: int | None = None,
            page_size: int | None = None,
            sort: list[str] | None = None
    ) -> list[dict[str, Any]] | None:
        """Получаем список моделей по поисковому запросу из индекса."""
        result: list[dict[str, Any]] = []
        try:
            docs = await self.elastic.search(
                index=index,
                query=query,
                sort=self._parse_sort(sort),
                size=page_size,
                from_=self._get_offset(page_number, page_size),
            )

        except NotFoundError:
            return None

        except BadRequestError as exp:
            raise exceptions.BadRequestError(
                status_code=exp.status_code,
                message=exp.message,
                body=exp.body,
                errors=exp.errors
            ) from exp

        for doc in docs["hits"]["hits"]:
            result.append(doc["_source"])
        return result

    async def _get_model(self, index: str, id_: str) -> dict[str, Any] | None:
        """Получаем данные о конкретной модели по id из индекса."""
        try:
            doc = await self.elastic.get(index=index, id=id_)

        except NotFoundError:
            return None

        except BadRequestError as exp:
            raise exceptions.BadRequestError(
                status_code=exp.status_code,
                message=exp.message,
                body=exp.body,
                errors=exp.errors
            ) from exp

        return doc["_source"]

    @staticmethod
    def _get_offset(
            page_number: int | None,
            page_size: int | None
    ) -> int | None:
        if page_number is not None and page_size is not None:
            return (page_number - 1) * page_size

        return None

    @staticmethod
    def _parse_sort(sort: list[str] | None) -> list[str] | None:
        if sort is not None:
            return [f"{item[1:]}:desc" if item.startswith("-") else item
                    for item in sort]
        return sort
