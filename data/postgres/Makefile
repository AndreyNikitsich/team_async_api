#!Make

include .env

POSTGRES_DB ?=
POSTGRES_USER ?=
POSTGRES_PASSWORD ?=

POSTGRES_DSN = postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}

build:
	docker build -t postgres .

run:
	docker run \
		--detach \
		--rm \
		--name postgres \
		--publish 5432:5432 \
		--env POSTGRES_DB=$(POSTGRES_DB) \
		--env POSTGRES_USER=$(POSTGRES_USER) \
		--env POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		postgres
	timeout 30s bash -c "until docker exec postgres pg_isready ; do sleep 5 ; done"

stop:
	docker stop postgres