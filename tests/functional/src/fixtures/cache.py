import pytest_asyncio
from functional.settings import test_settings
from redis.asyncio import Redis


@pytest_asyncio.fixture(scope="session")
async def cache_client():
    async with Redis(host=test_settings.REDIS_HOST, port=test_settings.REDIS_PORT) as client:
        yield client


@pytest_asyncio.fixture(scope="session", name="clear_cache")
async def clear_cache(cache_client):
    await cache_client.flushall()
