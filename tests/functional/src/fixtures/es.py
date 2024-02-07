import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from functional.settings import test_settings


@pytest_asyncio.fixture(scope="session", name="es_client")
async def es_client():
    async with AsyncElasticsearch(hosts=test_settings.ES_URL) as client:
        yield client


@pytest_asyncio.fixture(scope="session", name="clear_es_data")
async def clear_es_data(es_client: AsyncElasticsearch):
    await es_client.indices.delete(index="_all")
