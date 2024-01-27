from uuid import UUID

from asyncpg import Connection

from ..settings import fake


async def get_number_of_rows(connection: Connection, table: str) -> int:
    return await connection.fetchval(f'SELECT COUNT (*) FROM content.{table}')  # noqa: S608


async def _get_random_id_from_table(
    connection: Connection,
    table: str,
    number_of: int | None = None,
) -> UUID:
    if number_of is None:
        number_of = await get_number_of_rows(connection, table)
    cursor_offset = fake.random.randint(0, number_of - 1)
    async with connection.transaction():
        cursor = await connection.cursor(f'SELECT id FROM content.{table}')  # noqa: S608
        if cursor_offset > 0:
            await cursor.forward(cursor_offset)
        return (await cursor.fetchrow())[0]


async def get_random_genre_id(connection: Connection, number_of_genres: int | None = None) -> UUID:
    return await _get_random_id_from_table(connection, 'genre', number_of=number_of_genres)


async def get_random_person_id(connection: Connection, number_of_people: int | None = None) -> UUID:
    return await _get_random_id_from_table(connection, 'person', number_of=number_of_people)


async def get_random_definition_id(connection: Connection, number_of_definitions: int | None = None) -> UUID:
    return await _get_random_id_from_table(connection, 'definition', number_of=number_of_definitions)
