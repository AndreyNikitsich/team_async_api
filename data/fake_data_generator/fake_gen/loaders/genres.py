from datetime import datetime
from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.genre import GenreFactory
from ..models.genre import Genre
from .load_unrelated import load_unrelated


async def load_genres(connection: Connection, number_of: int, counter: Counter):
    def serialize_genre(  # noqa: WPS430
        genre: Genre,
    ) -> tuple[UUID, str, str, datetime, datetime]:
        return (
            genre['id'],
            genre['name'],
            genre['description'],
            genre['created'],
            genre['modified'],
        )

    query = """
        INSERT INTO content.genre (
            id,
            name,
            description,
            created,
            modified
        ) VALUES ($1, $2, $3, $4, $5);
    """
    await load_unrelated(connection, GenreFactory, query, serialize_genre, number_of, counter)
