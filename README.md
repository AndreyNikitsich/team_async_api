# Дорогой ревьювер!
У нас форс-мажор. 1 человек выбыл из команды и мы с трудом укладываемся в сроки.

IMPORTANT: Очень просим проверить вместе с заданием 4 спринта сразу и 5 (оставить комменты в репе),
чтобы мы не тратили время на отдельную итерацию по 5 спринту, а отправили уже поправленную версию.
Заранее спасибо !

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
