from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status
from services import exceptions
from services.genre import GenreService, get_genre_service

from .dependencies import PaginationParams, get_pagination_params
from .response_models import BaseGenreResponse, DetailGenreResponse

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get(
    "", summary="Получить список жанров", response_model=list[BaseGenreResponse], status_code=status.HTTP_200_OK
)
async def get_genres(
    pagination: PaginationParams = Depends(get_pagination_params),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[BaseGenreResponse]:
    try:
        genres = await genre_service.get_genres(page_number=pagination.page_number, page_size=pagination.page_size)
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    response = [BaseGenreResponse(uuid=genre.id, name=genre.name) for genre in genres]
    return response


@router.get(
    "/{genre_id}",
    summary="Получить детальную информация о жанре",
    response_model=DetailGenreResponse,
    status_code=status.HTTP_200_OK,
)
async def get_genre_info(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> DetailGenreResponse:
    try:
        genre = await genre_service.get_by_id(genre_id)
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    if genre is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    return DetailGenreResponse(uuid=genre.id, name=genre.name)
