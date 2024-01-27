import asyncio

import asyncpg

from .counter import Counter, output_counters
from .factories.related_to_film import RelatedToFilmFactory
from .loaders.cover import load_covers
from .loaders.definition import load_definitions
from .loaders.definition_film import load_definition_film
from .loaders.films import load_films
from .loaders.genre_film import load_genre_film
from .loaders.genres import load_genres
from .loaders.people import load_people
from .loaders.person_film import load_people_film
from .models.roles import Roles
from .providers.film_id import film_id_iterator
from .providers.random_id import get_number_of_rows


async def _generate_unrelated(pool: asyncpg.Pool, films: int, people: int, genres: int):  # noqa: WPS217,WPS210
    films_connection = await pool.acquire()
    people_connection = await pool.acquire()
    genres_connection = await pool.acquire()
    definitions_connection = await pool.acquire()

    films_counter = Counter('Films', films)
    people_counter = Counter('People', people)
    genres_counter = Counter('Genres', genres)
    definitions_counter = Counter('Definitions')

    counters_task = asyncio.create_task(output_counters([
        films_counter,
        people_counter,
        genres_counter,
        definitions_counter,
    ]))

    films_task = asyncio.create_task(load_films(films_connection, films, films_counter))
    people_task = asyncio.create_task(load_people(people_connection, people, people_counter))
    genres_task = asyncio.create_task(load_genres(genres_connection, genres, genres_counter))
    definitions_task = asyncio.create_task(load_definitions(definitions_connection, definitions_counter))

    await asyncio.gather(films_task, people_task, genres_task, definitions_task)
    counters_task.cancel()

    await pool.release(films_connection)
    await pool.release(people_connection)
    await pool.release(genres_connection)
    await pool.release(definitions_connection)


async def _generate_related(pool: asyncpg.Pool):  # noqa: WPS217,WPS210
    service_connection = await pool.acquire()
    genres_connection = await pool.acquire()
    definitions_connection = await pool.acquire()
    covers_connection = await pool.acquire()
    directors_connection = await pool.acquire()
    actors_connection = await pool.acquire()
    writers_connection = await pool.acquire()

    count_of_genres = await get_number_of_rows(service_connection, 'genre')
    count_of_people = await get_number_of_rows(service_connection, 'person')
    count_of_definitions = await get_number_of_rows(service_connection, 'definition')

    genres_counter = Counter('GenreFilm')
    definitions_counter = Counter('DefinitionFilm')
    covers_counter = Counter('CoverFilm')
    people_counter = Counter('PersonFilm')

    progress_task = asyncio.create_task(output_counters([
        genres_counter,
        definitions_counter,
        covers_counter,
        people_counter,
    ]))

    async for film_id in film_id_iterator(service_connection):
        related_to_film = RelatedToFilmFactory.build()
        tasks = [
            asyncio.create_task(load_genre_film(
                connection=genres_connection,
                film_id=film_id,
                number_of_genres=related_to_film['number_of_genres'],
                count_of_genres=count_of_genres,
                counter=genres_counter,
            )),
            asyncio.create_task(load_definition_film(
                connection=definitions_connection,
                film_id=film_id,
                number_of_definitions=related_to_film['number_of_definitions'],
                count_of_definitions=count_of_definitions,
                counter=definitions_counter,
            )),
            asyncio.create_task(load_covers(
                connection=covers_connection,
                film_id=film_id,
                counter=covers_counter,
            )),
            asyncio.create_task(load_people_film(
                connection=directors_connection,
                film_id=film_id,
                role=Roles.director,
                number_of_people=related_to_film['number_of_directors'],
                count_of_people=count_of_people,
                counter=people_counter,
            )),
            asyncio.create_task(load_people_film(
                connection=actors_connection,
                film_id=film_id,
                role=Roles.actor,
                number_of_people=related_to_film['number_of_actors'],
                count_of_people=count_of_people,
                counter=people_counter,
            )),
            asyncio.create_task(load_people_film(
                connection=writers_connection,
                film_id=film_id,
                role=Roles.writer,
                number_of_people=related_to_film['number_of_writers'],
                count_of_people=count_of_people,
                counter=people_counter,
            )),
        ]
        await asyncio.gather(*tasks)

    progress_task.cancel()

    await pool.release(service_connection)
    await pool.release(genres_connection)
    await pool.release(definitions_connection)
    await pool.release(covers_connection)
    await pool.release(directors_connection)
    await pool.release(actors_connection)
    await pool.release(writers_connection)


async def _do_work(dsn: str, films: int, people: int, genres: int):
    pool = await asyncpg.create_pool(dsn)
    await _generate_unrelated(pool, films, people, genres)
    await _generate_related(pool)
    await pool.close()


def do_work(dsn: str, films: int, people: int, genres: int):
    asyncio.get_event_loop().run_until_complete(_do_work(dsn, films, people, genres))
