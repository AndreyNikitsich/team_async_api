import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))
db_sqlite_path = os.getenv("DB_SQLITE", os.path.join(BASE_DIR, "db.sqlite"))

dsl = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", 5432),
    "options": "-c search_path=content",
}


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


@pytest.fixture
@contextmanager
def sqlite_context():
    conn = sqlite3.connect(db_sqlite_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
@contextmanager
def pg_context():
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def sqlite_cursor(sqlite_context):
    with sqlite_context as sqlite_conn:
        yield sqlite_conn.cursor()


@pytest.fixture
def pg_cursor(pg_context):
    with pg_context as pg_conn:
        yield pg_conn.cursor()
