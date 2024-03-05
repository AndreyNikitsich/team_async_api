# Async Api sprint 1
Async API - сервис асинхронного апи для кинотеатра.

## Local development
- Install python 3.11 (easy way is [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation))
- Install [poetry](https://python-poetry.org/docs/#installing-with-pipx)
- Run `cd src && poetry install` to create `.venv`
- ```cp .env.example .env  # edit if necessary```

## Run functional tests
```bash
docker-compose -f docker-compose-tests.yml up
```

## Start on production
```bash
cp .env.example .env  # edit if necessary
docker-compose up
```
