from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from redis.asyncio import Redis

from api import router as api_router
from core.config import settings
from db import elastic, redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis.REDIS_HOST, port=settings.redis.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[str(settings.es.ES_DSN)])
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.swagger.PROJECT_NAME,
    docs_url=settings.swagger.DOCS_URL,
    openapi_url=settings.swagger.OPENAPI_URL
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
