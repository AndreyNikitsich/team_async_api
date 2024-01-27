#!make

include .env

POSTGRES_DB ?=
POSTGRES_USER ?=
POSTGRES_PASSWORD ?=

POSTGRES_DSN = postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}

gen_small:
	poetry run python -m fake_gen --dsn ${POSTGRES_DSN} 1000 300 20

gen_large:
	poetry run python -m fake_gen --dsn ${POSTGRES_DSN} 200000 100000 200

flake8:
	poetry run flake8 fake_gen/

mypy:
	poetry run mypy fake_gen/

lint: flake8 mypy

isort:
	poetry run isort fake_gen/


format: isort
