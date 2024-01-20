from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.person_film import PersonFilmFactory
from ..models.roles import Roles
from ..providers.random_id import get_random_person_id


async def load_people_film(  # noqa: WPS211
    connection: Connection,
    film_id: UUID,
    role: Roles,
    number_of_people: int,
    count_of_people: int,
    counter: Counter,
):
    uuid_collection: set[UUID] = set()
    while len(uuid_collection) < number_of_people:
        uuid_collection.add(await get_random_person_id(connection, count_of_people))

    people_films = [
        PersonFilmFactory.build(film_id=film_id, person_id=person_id, role=role)
        for person_id in uuid_collection
    ]

    query = """
        INSERT INTO content.person_film (
            id,
            person_id,
            film_id,
            role,
            created,
            modified
        ) VALUES ($1, $2, $3, $4, $5, $6)
    """

    query_values = [
        (
            person_film['id'],
            person_film['person_id'],
            person_film['film_id'],
            person_film['role'].name,
            person_film['created'],
            person_film['modified'],
        ) for person_film in people_films
    ]

    await connection.executemany(query, query_values)
    await counter.inc(len(query_values))
