from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from redis.asyncio import Redis

from api import router as api_router
from core.config import settings
from db import elastic, redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)
    elastic.es = AsyncElasticsearch(hosts=[f"{settings.es.es_schema}://{settings.es.es_host}:{settings.es.es_port}"])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_metadata.project_name,
    docs_url=settings.project_metadata.docs_url,
    openapi_url=settings.project_metadata.openapi_url,
    version=settings.project_metadata.version,
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
