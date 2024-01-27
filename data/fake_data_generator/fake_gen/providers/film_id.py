from typing import AsyncIterator
from uuid import UUID

from asyncpg import Connection


async def film_id_iterator(connection: Connection) -> AsyncIterator[UUID]:
    async with connection.transaction():
        async for record in connection.cursor('SELECT id FROM content.film'):
            yield record[0]
