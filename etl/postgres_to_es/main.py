import time
from datetime import datetime

import backoff
import elasticsearch
import psycopg2
from clients.contexts import es_connect, pg_connect
from configs import config
from configs.logger import get_logger
from exraxtors.extract import PostgresExtractor
from loaders.loader import ElasticsearchLoader
from states.storage import JsonFileStorage, State
from transforms.transform import DataTransform

logger = get_logger(__name__)


def process(
        extractor: PostgresExtractor,
        transformer: DataTransform,
        loader: ElasticsearchLoader,
        state: State,
) -> None:
    """Процесс загрузки данных из Postgres в Elasticsearch"""
    last_modified = state.get_state("modified")
    logger.info(f"Последняя синхронизация {last_modified}")
    modified = last_modified or datetime.min

    for extracted_batch in extractor.extract(modified):
        data = transformer.transform(extracted_batch)
        loader.load(data)
        state.set_state("modified", str(datetime.now()))


@backoff.on_exception(backoff.expo,
                      (elasticsearch.exceptions.ConnectionError,
                       psycopg2.OperationalError),
                      max_tries=10,
                      logger=logger)
def main(pg_dsl: dict, es_dsl: dict):
    with pg_connect(**pg_dsl) as pg_conn, es_connect(**es_dsl) as es_client:
        state = State(JsonFileStorage(file_path=config.STATE_FILE_PATH))
        extractor = PostgresExtractor(
            connection=pg_conn,
            state=state,
            batch_size=config.BATCH_SIZE
        )
        transformer = DataTransform()
        loader = ElasticsearchLoader(es_client=es_client)

        process(
            extractor=extractor,
            transformer=transformer,
            loader=loader,
            state=state
        )


if __name__ == "__main__":
    try:
        while True:
            main(config.POSTGRES_DSL, config.ELASTICSEARCH_DSL)
            logger.info(f"Пауза: {config.SLEEP_TIME} сек.")
            time.sleep(config.SLEEP_TIME)
    except KeyboardInterrupt:
        logger.info("Завершаем работу...")
