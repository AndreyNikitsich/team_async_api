from contexts import cursor_connect
from dto_factory import factory


class SQLiteExtractor:
    def __init__(self, connection):
        self.connection = connection

    def extract_movies(self, size=500):
        for table_name in self.tables:
            yield from self.get_data_table(size, table_name)

    def get_data_table(self, size, table_name):
        with cursor_connect(self.connection) as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            while True:
                result = cursor.fetchmany(size)
                if not result:
                    break
                data = [factory.create(
                    table_name, **dict(row)
                ) for row in result]

                yield table_name, data

    @property
    def tables(self):
        return [*factory.registered()]
