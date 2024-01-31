from contextlib import asynccontextmanager

import uvicorn
from api import router as api_router
from core.config import settings
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis.REDIS_HOST, port=settings.redis.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f"{settings.es.ES_SCHEMA}://{settings.es.ES_HOST}:{settings.es.ES_PORT}"])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.swagger.PROJECT_NAME,
    docs_url=settings.swagger.DOCS_URL,
    openapi_url=settings.swagger.OPENAPI_URL,
)

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
