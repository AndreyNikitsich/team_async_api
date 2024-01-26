from datetime import datetime
from uuid import UUID

from asyncpg import Connection

from ..counter import Counter
from ..factories.definition import DEFINITIONS_COLLECTION_LEN, DefinitionFactory
from ..models.definition import Definition
from .load_unrelated import load_unrelated


async def load_definitions(connection: Connection, counter: Counter):
    def serialize_definition(  # noqa: WPS430
        genre: Definition,
    ) -> tuple[UUID, str, datetime, datetime]:
        return (
            genre['id'],
            genre['name'],
            genre['created'],
            genre['modified'],
        )

    query = """
        INSERT INTO content.definition (
            id,
            name,
            created,
            modified
        ) VALUES ($1, $2, $3, $4);
    """
    await load_unrelated(
        connection,
        DefinitionFactory,
        query,
        serialize_definition,
        DEFINITIONS_COLLECTION_LEN,
        counter,
    )
