from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from fake_data.services_contracts.film_service import FilmService, get_film_service
from fake_data.services_contracts.person_service import PersonService, get_person_service

from .dependencies import PaginationParams, get_pagination_params
from .response_models import PersonBase, PersonInfo, PersonsFilm

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/{person_id}", response_model=PersonInfo, status_code=status.HTTP_200_OK)
async def get_person_info(person_id: UUID, person_service: PersonService = Depends(get_person_service)) -> PersonInfo:
    person = await person_service.get_by_id(person_id)
    if person is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return PersonInfo(
        uuid=person.id,
        full_name=person.name,
    )


@router.get("/{person_id}/films", response_model=list[PersonsFilm], status_code=status.HTTP_200_OK)
async def get_films_for_person(
    person_id: UUID,
    pagination_params: PaginationParams = Depends(get_pagination_params),
    film_service: FilmService = Depends(get_film_service),
) -> list[PersonsFilm]:
    films = await film_service.get_films_for_person(
        person_id=person_id,
        page_size=pagination_params.page_size,
        page_number=pagination_params.page_number,
    )
    response = [
        PersonsFilm(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating, roles=film.roles) for film in films
    ]
    return response


@router.get("/search", response_model=list[PersonBase], status_code=status.HTTP_200_OK)
async def search_person_by_query(
    query: str,
    pagination_params: PaginationParams = Depends(get_pagination_params),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonBase]:
    persons = await person_service.get_by_search(
        query=query, page_number=pagination_params.page_number, page_size=pagination_params.page_size
    )
    response = [PersonBase(uuid=person.id, full_name=person.name) for person in persons]
    return response
