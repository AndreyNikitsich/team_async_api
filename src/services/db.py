from typing import Annotated, Any, List, Optional, Type

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import BaseModel as Model


class ElasticService:
    """Содержит бизнес-логику по работе с Elasticsearch."""

    def __init__(self, elastic: Annotated[AsyncElasticsearch, Depends(get_elastic)]):
        self.elastic = elastic

    async def search_models(
            self,
            model: Type[Model],
            index: str,
            query: Optional[dict[str, Any]] = None,
            page_number: Optional[int] = None,
            page_size: Optional[int] = None,
            sort: Optional[List[str]] = None
    ) -> List[Any]:
        """Получаем список моделей по поисковому запросу из индекса."""
        models: List[Model] = []
        try:
            docs = await self.elastic.search(
                index=index,
                query=query,
                sort=self._parse_sort(sort),
                size=page_size,
                from_=self._get_offset(page_number, page_size),
            )
        except NotFoundError:
            return models

        for doc in docs["hits"]["hits"]:
            models.append(model(**doc["_source"]))
        return models

    async def get_model(
            self,
            model: Type[Model],
            index: str,
            id_: str,

    ) -> Optional[Model]:
        """Получаем данные о конкретной модели по id из индекса."""
        try:
            doc = await self.elastic.get(
                index=index,
                id=id_
            )
        except NotFoundError:
            return None

        return model(**doc["_source"])

    @staticmethod
    def _get_offset(
            page_number: Optional[int],
            page_size: Optional[int]
    ) -> Optional[int]:
        if page_number is not None and page_size is not None:
            return (page_number - 1) * page_size

        return None

    @staticmethod
    def _parse_sort(sort: Optional[List[str]]) -> Optional[List[str]]:
        if sort is not None:
            return [f"{item[1:]}:desc" if item.startswith("-") else item
                    for item in sort]
        return sort
