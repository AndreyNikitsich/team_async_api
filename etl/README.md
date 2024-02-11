# ETL загрузки данных в Elasticsearch из PostgresQL

Загружает данные в Elasticsearch из PostgresQL.

### Run
```shell
docker compose -f docker-compose.prod.yml up -d --build
```

### Elasticsearch
http://localhost:9200/movies/_search?pretty

### Postman test
https://code.s3.yandex.net/middle-python/learning-materials/ETLTests-2.json