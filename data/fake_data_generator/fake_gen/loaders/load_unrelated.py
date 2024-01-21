from typing import Any, Callable

import asyncpg
from polyfactory.factories import TypedDictFactory

from ..counter import Counter
from ..settings import CHUNK_SIZE


async def load_unrelated(  # noqa: WPS211
    connection: asyncpg.Connection,
    factory: type[TypedDictFactory],
    query: str,
    row_serializer: Callable[[Any], tuple[Any, ...]],
    number_of: int,
    counter: Counter,
    chunk_size: int = CHUNK_SIZE,
):
    left_to_load = number_of
    while left_to_load > 0:
        chunk_to_load = min(left_to_load, chunk_size)

        chunk_data = [
            row_serializer(factory.build())
            for _ in range(chunk_to_load)
        ]
        await connection.executemany(query, chunk_data)

        left_to_load -= chunk_to_load
        await counter.inc(chunk_to_load)
