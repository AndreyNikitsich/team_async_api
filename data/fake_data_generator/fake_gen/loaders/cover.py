from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.cover import CoverFactory


async def load_covers(
    connection: Connection,
    film_id: UUID,
    counter: Counter,
):
    covers = [
        CoverFactory.build(film_id=film_id, size='320x240', url='https://fakeimg.pl/320x240/'),
        CoverFactory.build(film_id=film_id, size='800x600', url='https://fakeimg.pl/800x600/'),
    ]

    query = """
        INSERT INTO content.cover (
            id,
            film_id,
            size,
            url,
            created,
            modified
        ) VALUES ($1, $2, $3, $4, $5, $6)
    """

    query_values = [
        (
            cover['id'],
            cover['film_id'],
            cover['size'],
            cover['url'],
            cover['created'],
            cover['modified'],
        )
        for cover in covers
    ]

    await connection.executemany(query, query_values)
    await counter.inc(len(query_values))
