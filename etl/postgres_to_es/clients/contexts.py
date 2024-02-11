from contextlib import contextmanager

import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extras import RealDictCursor


@contextmanager
def pg_connect(**dsl: dict):
    """Контекст менеджер соединения PostgresQL."""
    conn = psycopg2.connect(**dsl, cursor_factory=RealDictCursor)
    conn.set_session(autocommit=True)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_cursor_connect(connection):
    """Контекст менеджер курсора для соединения DB."""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


@contextmanager
def es_connect(**dsl: dict):
    """Контекст менеджер соединения Elasticsearch."""
    es_connection = Elasticsearch(**dsl)
    try:
        yield es_connection
    finally:
        es_connection.close()
