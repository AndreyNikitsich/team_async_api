# ruff: noqa: ERA001
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status

from services import exceptions
from services.person import PersonService, get_person_service

from .dependencies import PaginationParams, get_pagination_params
from .response_models import BasePersonResponse, DetailPersonResponse, PersonsFilmResponse

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get(
    "/{person_id}",
    summary="Получить детальную информация о персоне",
    response_model=DetailPersonResponse,
    status_code=status.HTTP_200_OK,
)
async def get_person_info(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> DetailPersonResponse:
    try:
        person = await person_service.get_by_id(person_id)
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    if person is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")

    return DetailPersonResponse(
        uuid=person.id,
        full_name=person.full_name,
    )


@router.get(
    "/{person_id}/films",
    summary="Получить список фильмов, в которых персона принимала участие",
    response_model=list[PersonsFilmResponse],
    status_code=status.HTTP_200_OK,
)
async def get_films_for_person(
    person_id: str,
    pagination_params: PaginationParams = Depends(get_pagination_params),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonsFilmResponse]:
    persons_with_films = await person_service.get_films_for_person(
        person_id=person_id,
        page_size=pagination_params.page_size,
        page_number=pagination_params.page_number,
    )
    response = [
        PersonsFilmResponse(uuid=person.id, title=person.title, imdb_rating=person.imdb_rating, roles=person.roles)
        for person in persons_with_films
    ]
    return response


@router.get(
    "/search",
    summary="Полнотекстовый поиск по персоналиям",
    response_model=list[BasePersonResponse],
    status_code=status.HTTP_200_OK,
)
async def search_person_by_query(
    query: str,
    pagination: PaginationParams = Depends(get_pagination_params),
    person_service: PersonService = Depends(get_person_service),
) -> list[BasePersonResponse]:
    try:
        persons = await person_service.get_by_search(
            query=query, page_number=pagination.page_number, page_size=pagination.page_size
        )
    except exceptions.BadRequestError as ex:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    response = [BasePersonResponse(uuid=person.id, full_name=person.full_name) for person in persons]
    return response
