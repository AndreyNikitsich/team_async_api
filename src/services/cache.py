import hashlib
import json
from typing import Any

from core.config import settings
from db.redis import get_redis

cache_provider = get_redis


class CacheService:
    """Содержит бизнес-логику по работе с кешем."""

    @staticmethod
    async def get_cache(key: str) -> dict[str, Any] | None:
        """Получаем данные запроса из кеша."""
        provider = await cache_provider()
        data = await provider.get(key)
        if not data:
            return None

        return json.loads(data.decode("utf-8"))

    @staticmethod
    async def put_cache(key: str, data: str):
        """Сохраняем данные запроса в кеше."""
        provider = await cache_provider()
        await provider.set(key, data, settings.redis.CACHE_EXPIRE_IN_SECONDS)


class QueryCache(CacheService):
    """Декоратор, кеширует поисковые запросы к базе данных."""

    def __call__(self, func):
        async def cached(*args, **kwargs):
            m = hashlib.sha256()
            for arg in kwargs.values():
                m.update(bytes(str(arg), "utf-8"))
            cache_key = m.hexdigest()

            result = await self.get_cache(cache_key)
            if not result:
                result = await func(*args, **kwargs)
                if not result:
                    return None
                await self.put_cache(cache_key, json.dumps(result))

            return result

        return cached


class ModelCache(CacheService):
    """Декоратор, кеширует данные модели при запросах к базе данных."""

    def __init__(self, *, key: str = ""):
        self.key = key

    def __call__(self, func):
        async def cached(*args, **kwargs):
            cache_key = kwargs.get(self.key)
            if not cache_key:
                cache_key = "".join(tuple(kwargs.values()))

            result = await self.get_cache(cache_key)
            if not result:
                result = await func(*args, **kwargs)
                if not result:
                    return None
                await self.put_cache(cache_key, json.dumps(result))

            return result

        return cached
