from typing import Annotated, Type

from core.config import settings
from db.redis import get_redis
from fastapi import Depends
from pydantic import BaseModel as Model
from redis.asyncio import Redis


class CacheService:
    """Содержит бизнес-логику по работе с кешем."""

    def __init__(self, redis: Annotated[Redis, Depends(get_redis)]):
        self.redis = redis

    async def get_query_cache(self, key: str):
        """Получаем данные запроса из кеша."""

    async def put_query_cache(self):
        """Сохраняем данные запроса в кеш."""

    async def get_model_cache(self, key: str, model: Type[Model]):
        """Получаем данные конкретной модели из кеша."""
        data = await self.redis.get(key)
        if not data:
            return None

        model_data = model.model_validate_json(data)
        return model_data

    async def put_model_cache(self, key: str, model: Model):
        """Сохраняем данные конкретной модели в кеше."""
        await self.redis.set(key, model.model_dump_json(),
                             settings.redis.CACHE_EXPIRE_IN_SECONDS)
