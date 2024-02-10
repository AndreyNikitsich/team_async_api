from typing import Any

from configs.logger import get_logger
from elasticsearch import Elasticsearch, helpers

logger = get_logger(__name__)


class ElasticsearchLoader:
    """Загружает данные полученные из PostgresQL пачками в Elasticsearch."""

    def __init__(self, es_client: Elasticsearch):
        self.es_client = es_client

    def load(self, data: tuple[str, list[dict[str, Any]]]):
        index, data_ = data

        def get_actions(docs):
            for doc in docs:
                action = {
                    "_index": index,
                    "_op_type": "index",
                    "_id": doc["id"],
                    "_source": doc,
                }
                yield action

        helpers.bulk(self.es_client, get_actions(data_))
        logger.info(f"Загружено в индекс `{index}` {len(data_)} строк")
