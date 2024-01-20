import asyncio

import asyncpg


async def _generate_unrelated(pool: asyncpg.Pool, films: int, people: int, genres: int):
    pass


async def _generate_related(pool: asyncpg.Pool):
    pass


async def _do_work(dsn: str, films: int, people: int, genres: int):
    pool = await asyncpg.create_pool(dsn)
    await _generate_unrelated(pool, films, people, genres)
    await _generate_related(pool)
    await pool.close()


def do_work(dsn: str, films: int, people: int, genres: int):
    asyncio.get_event_loop().run_until_complete(_do_work(dsn, films, people, genres))
