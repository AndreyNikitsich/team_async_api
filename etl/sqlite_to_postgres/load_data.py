import logging
import os
import sqlite3

from contexts import pg_context, sqlite_context
from dotenv import load_dotenv
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from sqlite_extractor import SQLiteExtractor


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    dsl = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", 5432),
        "options": "-c search_path=content",
    }
    db_sqlite_path = os.getenv("DB_SQLITE", "db.sqlite")

    with sqlite_context(db_sqlite_path) as sqlite_conn, \
            pg_context(**dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
