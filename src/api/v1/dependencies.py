from fastapi import Query
from pydantic import BaseModel

from core.config import settings


class PaginationParams(BaseModel):
    page_number: int
    page_size: int


def get_pagination_params(
    page_number: int = Query(settings.api.default_page_number, gt=0),
    page_size: int = Query(settings.api.default_page_size, gt=0),
) -> PaginationParams:
    return PaginationParams(page_number=page_number, page_size=page_size)
