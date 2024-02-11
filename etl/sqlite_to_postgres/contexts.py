import sqlite3
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


@contextmanager
def sqlite_context(db_path: str):
    """Контекст менеджер соединения Sqlite."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_context(**dsl):
    """Контекст менеджер соединения PostgresQL."""
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def cursor_connect(connection):
    """Контекст менеджер курсора для соединения DB."""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
