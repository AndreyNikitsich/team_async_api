from typing import Iterator

import sql_query
from clients.contexts import pg_cursor_connect
from configs.logger import get_logger
from psycopg2.extensions import connection as _connection
from states.storage import State

logger = get_logger(__name__)


class PostgresExtractor:
    """Получает данные из PostgresQL."""

    def __init__(self, connection: _connection, state: State,
                 batch_size: int) -> None:
        self.connection = connection
        self.state = state
        self.batch_size = batch_size

    def extract(self, modified_data) -> Iterator:
        """
        Извлекает измененные данные из базы данных
        пачками за определенный промежуток времени.
        """
        with pg_cursor_connect(self.connection) as cursor:

            queries = (
                (
                    "movies",
                    (
                        sql_query.movies,
                        (modified_data, modified_data, modified_data)
                    )
                ),
                (
                    "genres",
                    (
                        sql_query.genres, (modified_data,)
                    )
                ),
                (
                    "persons",
                    (
                        sql_query.persons, (modified_data,)
                    )
                ),
            )

            for index, query_ in queries:
                query = cursor.mogrify(*query_)
                cursor.execute(query)

                while True:
                    rows = cursor.fetchmany(self.batch_size)
                    if not rows:
                        logger.info(f"Изменения в `{index}` не обнаружены.")
                        break

                    logger.info(f"Извлечено из `{index}` {len(rows)} строк")
                    yield index, rows
