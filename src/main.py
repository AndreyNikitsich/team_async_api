import logging
from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from redis.asyncio import Redis

from api import router as api_router
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis.REDIS_HOST, port=settings.redis.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f"{settings.es.ES_SCHEMA}://{settings.es.ES_HOST}:{settings.es.ES_PORT}"])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_metadata.PROJECT_NAME,
    docs_url=settings.project_metadata.DOCS_URL,
    openapi_url=settings.project_metadata.OPENAPI_URL,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
