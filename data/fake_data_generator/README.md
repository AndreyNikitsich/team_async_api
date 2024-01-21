# Утилита для генерации фейковых данных

* Пакетный менеджер: `Poetry`
* Провайдер данных: `Faker`
* Работа с БД: `asyncpg`

Утилита выполнена в виде асинхронного приложения, 
реализована конкурентная работа с пулом подключений к БД.
Используется один физический процессор.

## Usage

```shell
usage: fake_gen [-h] [--dsn DSN] [-v] films people genres

Fake data generator version 0.1.0

positional arguments:
  films          Number of films
  people         Number of people
  genres         Number of genres

options:
  -h, --help     show this help message and exit
  --dsn DSN      Postgresql connection string
  -v, --version  Show self version and exit

Have a nice day!
```

## Переменные окружения

Для локальной разработки необходимо создать файл .env

(см. пример [.env.example](./.env.example) )

## Команды make

### Сгенерировать 1000 фильмов 300 персон и 20 жанров

```shell
make gen_small
```

### Сгенерировать 200к фильмов 100к актеров и 200 жанров

```shell
make gen_large
```

>Внимание! Генерация большого количества данных занимает продолжительное время

### Запуск линтеров

```shell
make flake8
make mypy
```
```shell
make lint
```

### Запуск форматеров

```shell
make isort
```

```shell
make format
```
