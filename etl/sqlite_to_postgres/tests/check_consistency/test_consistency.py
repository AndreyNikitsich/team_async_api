import pytest


@pytest.mark.parametrize(
    "table_name",
    ["film_work", "genre", "person", "genre_film_work", "person_film_work"]
)
def test_data_integrity(sqlite_cursor, pg_cursor, table_name):
    """
    Проверка целостности данных между каждой
    парой таблиц в SQLite и Postgres.
    """
    query = f"SELECT * FROM {table_name};"
    sqlite_cursor.execute(query)
    pg_cursor.execute(query)

    assert len(sqlite_cursor.fetchall()) == len(pg_cursor.fetchall()), (
        f"Количество записей в таблице {table_name} не совпадают.")


@pytest.mark.parametrize(
    "table_name",
    ["film_work", "genre", "person", "genre_film_work", "person_film_work"]
)
def test_content_records(sqlite_cursor, pg_cursor, table_name):
    """Проверка содержимого записей внутри каждой таблицы."""
    pg_cursor.execute(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'content' AND table_name = '{table_name}';
    """)

    pg_column_names = [name[0] for name in pg_cursor.fetchall()]

    sqlite_cursor.execute(
        f"SELECT name FROM pragma_table_info('{table_name}')")
    sqlite_column_names = [name[0] for name in sqlite_cursor.fetchall()]

    column_names = ", ".join(
        list(set(pg_column_names) & set(sqlite_column_names)))

    pg_cursor.execute(
        f"SELECT {column_names} FROM content.{table_name} ORDER BY id")
    pg_data = [tuple(row) for row in pg_cursor.fetchall()]

    sqlite_cursor.execute(
        f"SELECT {column_names} FROM {table_name} ORDER BY id")
    sqlite_data = [tuple(row) for row in sqlite_cursor.fetchall()]

    assert pg_data == sqlite_data, (
        f"Данные в таблице {table_name} не совпадают.")
