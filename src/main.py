import uvicorn
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from api import router as api_router
from core.config import settings
from fastapi import FastAPI

from db import redis, elastic

from logging import getLogger

logger = getLogger(__name__)

app = FastAPI(
    title=settings.swagger.PROJECT_NAME, docs_url=settings.swagger.DOCS_URL, openapi_url=settings.swagger.OPENAPI_URL
)

app.include_router(api_router, prefix="/api")

@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=settings.redis.REDIS_HOST, port=settings.redis.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f"{settings.es.ES_SCHEMA}://{settings.es.ES_HOST}:{settings.es.ES_PORT}"])
    logger.info(redis.redis)

@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
