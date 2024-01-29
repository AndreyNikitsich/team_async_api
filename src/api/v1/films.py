from enum import Enum
from http import HTTPStatus
from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from fake_data.services_contracts.film_service import FilmService, get_film_service

from .dependencies import PaginationParams, get_pagination_params
from .response_models import FilmBase, FilmInfo

router = APIRouter(tags=["films"])


class AvailableSorting(str, Enum):
    IMDB_RATING_ASC = "imdb_rating"
    IMDB_RATING_DESC = "-imdb_rating"


@router.get("/films", response_model=list[FilmBase], status_code=status.HTTP_200_OK)
async def get_films(
    # Can't see list parameters as array in openapi, may be related to https://github.com/tiangolo/fastapi/issues/10999
    sort: Annotated[list[AvailableSorting] | None, Query()] = None,
    genre: Annotated[list[str] | None, Query()] = None,
    pagination_params: PaginationParams = Depends(get_pagination_params),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmBase]:
    films = await film_service.get_films(
        sorting_fields=cast(list[str], sort),
        page_size=pagination_params.page_size,
        page_number=pagination_params.page_number,
        genres=genre,
    )
    response = [FilmBase(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
    return response


@router.get("/films/search", response_model=list[FilmBase], status_code=status.HTTP_200_OK)
async def search_film_by_query(
    query: str,
    pagination_params: PaginationParams = Depends(get_pagination_params),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmBase]:
    films = await film_service.get_by_search(
        query=query,
        page_size=pagination_params.page_size,
        page_number=pagination_params.page_number,
    )
    response = [FilmBase(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]
    return response


@router.get("/films/{film_id}", response_model=FilmInfo, status_code=status.HTTP_200_OK)
async def get_film_info(film_id: UUID, film_service: FilmService = Depends(get_film_service)) -> FilmInfo:
    film = await film_service.get_by_id(film_id)
    if film is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return FilmInfo(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[],
        actors=[],
        writers=[],
        directors=[],
    )
