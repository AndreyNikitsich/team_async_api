from datetime import datetime
from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.film import FilmFactory
from ..loaders.load_unrelated import load_unrelated
from ..models.film import Film


async def load_films(connection: Connection, number_of: int, counter: Counter):
    def serialize_film(  # noqa: WPS430
        film: Film,
    ) -> tuple[UUID, str, float, datetime, str, datetime, datetime]:
        return (  # noqa: WPS227
            film['id'],
            film['title'],
            film['imdb_rating'],
            film['release_date'],
            film['description'],
            film['created'],
            film['modified'],
        )

    query = """
        INSERT INTO content.film (
            id,
            title,
            imdb_rating,
            release_date,
            description,
            created,
            modified
        ) VALUES ($1, $2, $3, $4, $5, $6, $7);
    """
    await load_unrelated(connection, FilmFactory, query, serialize_film, number_of, counter)
