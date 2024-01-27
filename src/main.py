import uvicorn
from api import router as api_router
from core.config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.project_metadata.PROJECT_NAME,
    docs_url=settings.project_metadata.DOCS_URL,
    openapi_url=settings.project_metadata.OPENAPI_URL,
    version=settings.project_metadata.VERSION,
)

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
    )
