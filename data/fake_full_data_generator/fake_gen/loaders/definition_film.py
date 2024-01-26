from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.definition_film import DefinitionFilmFactory
from ..providers.random_id import get_random_definition_id


async def load_definition_film(
    connection: Connection,
    film_id: UUID,
    number_of_definitions: int,
    count_of_definitions: int,
    counter: Counter,
):
    uuid_collection: set[UUID] = set()
    while len(uuid_collection) < number_of_definitions:
        uuid_collection.add(await get_random_definition_id(connection, count_of_definitions))

    definitions_films = [
        DefinitionFilmFactory.build(film_id=film_id, definition_id=definition_id)
        for definition_id in uuid_collection
    ]

    query = """
        INSERT INTO content.definition_film (
            id,
            definition_id,
            film_id,
            created
        ) VALUES ($1, $2, $3, $4);
    """

    query_values = [
        (
            definition_film['id'],
            definition_film['definition_id'],
            definition_film['film_id'],
            definition_film['created'],
        ) for definition_film in definitions_films
    ]

    await connection.executemany(query, query_values)
    await counter.inc(len(query_values))
