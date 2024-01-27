from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.genre_film import GenreFilmFactory
from ..providers.random_id import get_random_genre_id


async def load_genre_film(
    connection: Connection,
    film_id: UUID,
    number_of_genres: int,
    count_of_genres: int,
    counter: Counter,
):
    uuid_collection: set[UUID] = set()
    while len(uuid_collection) < number_of_genres:
        uuid_collection.add(await get_random_genre_id(connection, count_of_genres))

    genres_films = [GenreFilmFactory.build(film_id=film_id, genre_id=genre_id) for genre_id in uuid_collection]

    query = """
        INSERT INTO content.genre_film (
            id,
            genre_id,
            film_id,
            created
        ) VALUES ($1, $2, $3, $4);
    """

    query_values = [
        (
            genre_film['id'],
            genre_film['genre_id'],
            genre_film['film_id'],
            genre_film['created'],
        )
        for genre_film in genres_films
    ]

    await connection.executemany(query, query_values)
    await counter.inc(len(query_values))
