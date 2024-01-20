from datetime import datetime
from uuid import UUID

from asyncpg import Connection

from .load_unrelated import load_unrelated
from ..counter import Counter
from ..factories.person import PersonFactory
from ..models.person import Person


async def load_people(connection: Connection, number_of: int, counter: Counter):
    def serialize_person(  # noqa: WPS430
        person: Person,
    ) -> tuple[UUID, str, datetime, datetime]:
        return (
            person['id'],
            person['full_name'],
            person['created'],
            person['modified'],
        )

    query = """
        INSERT INTO content.person (
            id,
            full_name,
            created,
            modified
        ) VALUES ($1, $2, $3, $4);
    """
    await load_unrelated(connection, PersonFactory, query, serialize_person, number_of, counter)
