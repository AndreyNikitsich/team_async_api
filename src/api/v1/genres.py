from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from fake_data.services_contracts.genre_service import GenreService, get_genre_service

from .response_models import GenreBase, GenreInfo

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("", response_model=list[GenreBase], status_code=status.HTTP_200_OK)
async def get_genres(genre_service: GenreService = Depends(get_genre_service)) -> list[GenreBase]:
    genres = await genre_service.get_genres()
    response = [GenreBase(uuid=genre.id, name=genre.name) for genre in genres]
    return response


@router.get("/{genre_id}", response_model=GenreInfo, status_code=status.HTTP_200_OK)
async def get_genre_info(genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)) -> GenreInfo:
    genre = await genre_service.get_by_id(genre_id)
    if genre is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")
    return GenreInfo(uuid=genre.id, name=genre.name)
