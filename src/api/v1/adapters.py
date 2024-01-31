from models.film import Film, FilmGenres, FilmPerson

from api.v1.response_models import BaseGenreResponse, BasePersonResponse, DetailFilmResponse


def film_person_to_base_person_response(person: FilmPerson):
    return BasePersonResponse(uuid=person.id, full_name=person.name)


def film_genre_to_base_genre_response(genre: FilmGenres):
    return BaseGenreResponse(uuid=genre.id, name=genre.name)


def film_to_detail_film_response(film: Film):
    return DetailFilmResponse(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description if film.description is not None else "",
        genres=[film_genre_to_base_genre_response(genre) for genre in film.genres],
        actors=[film_person_to_base_person_response(person) for person in film.actors],
        writers=[film_person_to_base_person_response(person) for person in film.writers],
        directors=[film_person_to_base_person_response(person) for person in film.directors],
    )


ADAPTERS = {
    Film: film_to_detail_film_response,
}
