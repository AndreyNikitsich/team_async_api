import logging
from dataclasses import astuple, fields

from contexts import cursor_connect

logger = logging.getLogger(__name__)


class PostgresSaver:
    def __init__(self, connection):
        self.connection = connection

    def save_all_data(self, data):
        for table_name, dto_list in data:
            with cursor_connect(self.connection) as cursor:
                column_names = [field.name for field in fields(dto_list[0])]
                column_names_str = ",".join(column_names)
                col_count = ", ".join(["%s"] * len(column_names))
                bind_values = ",".join(
                    cursor.mogrify(
                        f"({col_count})",
                        astuple(dto)
                    ).decode("utf-8") for dto in dto_list)

                query = (f"""
                INSERT INTO content.{table_name} ({column_names_str})
                VALUES {bind_values}
                ON CONFLICT (id) DO NOTHING
                """)
                cursor.execute(query)

        self.connection.commit()
        logger.info("Данные загружены...")
