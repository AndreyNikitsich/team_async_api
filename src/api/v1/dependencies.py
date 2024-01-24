from core.config import settings
from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page_number: int
    page_size: int


def get_pagination_params(
    page_number: int = Query(settings.api.DEFAULT_PAGE_NUMBER, gt=0),
    page_size: int = Query(settings.api.DEFAULT_PAGE_SIZE, gt=0),
) -> PaginationParams:
    return PaginationParams(page_number=page_number, page_size=page_size)
