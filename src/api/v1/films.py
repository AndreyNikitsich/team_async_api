from enum import Enum
from http import HTTPStatus
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, Query, status

from models.film import Film
from services import exceptions
from services.film import FilmService, get_film_service

from .adapters import ADAPTERS
from .dependencies import PaginationParams, get_pagination_params
from .response_models import BaseFilmResponse, DetailFilmResponse

router = APIRouter(tags=["films"])


class AvailableSorting(str, Enum):
    IMDB_RATING_ASC = "imdb_rating"
    IMDB_RATING_DESC = "-imdb_rating"


@router.get(
    "/films",
    summary="Получить список фильмов удовлетворяющий параметрам",
    response_model=list[BaseFilmResponse],
    status_code=status.HTTP_200_OK,
)
async def get_films(
    sort: Annotated[list[AvailableSorting], Query()] = AvailableSorting.IMDB_RATING_DESC,  # type: ignore
    genre: Annotated[list[str], Query()] = None,  # type: ignore
    pagination: PaginationParams = Depends(get_pagination_params),
    film_service: FilmService = Depends(get_film_service),
) -> list[BaseFilmResponse]:
    try:
        films: list[Film] = await film_service.get_films(
            sort=cast(list[str], sort), genre=genre, page_number=pagination.page_number, page_size=pagination.page_size
        )
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    response = [BaseFilmResponse(uuid=film.id, title=film.title, genres=film.genres_names,
                                 imdb_rating=film.imdb_rating) for film in films]
    return response


@router.get(
    "/films/search",
    summary="Полнотекстовый поиск по фильмам",
    response_model=list[BaseFilmResponse],
    status_code=status.HTTP_200_OK,
)
async def search_film_by_query(
    query: str,
    sort: Annotated[list[AvailableSorting], Query()] = AvailableSorting.IMDB_RATING_DESC,  # type: ignore
    pagination_params: PaginationParams = Depends(get_pagination_params),
    film_service: FilmService = Depends(get_film_service),
) -> list[BaseFilmResponse]:
    try:
        films = await film_service.get_by_search(
            query=query,
            sort=cast(list[str], sort),
            page_number=pagination_params.page_number,
            page_size=pagination_params.page_size,
        )
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    response = [BaseFilmResponse(uuid=film.id, title=film.title, genres=film.genres_names,
                                 imdb_rating=film.imdb_rating) for film in films]
    return response


@router.get(
    "/films/{film_id}",
    summary="Получить детальную информацию о фильме",
    response_model=DetailFilmResponse,
    status_code=status.HTTP_200_OK,
)
async def get_film_info(film_id: str, film_service: FilmService = Depends(get_film_service)) -> DetailFilmResponse:
    try:
        film = await film_service.get_by_id(film_id)
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    if film is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")

    return ADAPTERS[type(film)](film)
