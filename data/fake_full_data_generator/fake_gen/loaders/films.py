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
    ) -> tuple[UUID, str, float, str, list[str], int, datetime, str, datetime, datetime]:
        return (  # noqa: WPS227
            film['id'],
            film['title'],
            film['imdb_rating'],
            str(film['mpaa_rating'].value),
            [str(accessibility.value) for accessibility in film['accessibility_features']],
            film['duration_settings'],
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
            mpaa_rating,
            accessibility_features,
            duration_settings,
            release_date,
            description,
            created,
            modified
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
    """
    await load_unrelated(connection, FilmFactory, query, serialize_film, number_of, counter)
