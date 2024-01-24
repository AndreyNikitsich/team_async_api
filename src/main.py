import uvicorn
from api import router as api_router
from core.config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.swagger.PROJECT_NAME, docs_url=settings.swagger.DOCS_URL, openapi_url=settings.swagger.OPENAPI_URL
)

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
