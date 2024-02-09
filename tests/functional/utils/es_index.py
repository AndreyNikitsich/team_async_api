import time

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from functional.settings import TestSettings


class ESIndex:
    def __init__(self, client: AsyncElasticsearch, test_config: TestSettings):
        self.client = client
        self.index = test_config.ES_INDEX
        self.index_mapping = test_config.ES_INDEX_MAPPING

    async def create(self):
        await self.client.indices.create(
            index=self.index, **self.index_mapping)

    async def update(self, es_data):
        updated, errors = await async_bulk(client=self.client, actions=es_data)
        time.sleep(2)
        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    async def delete(self):
        if await self.client.indices.exists(index=self.index):
            await self.client.indices.delete(index=self.index)

    async def check(self):
        await self.client.indices.stats(index=self.index, metric="indexing")
