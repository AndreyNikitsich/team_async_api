build:
	docker build --tag elasticsearch .

run:
	docker run --detach --rm --publish 9200:9200 --name elasticsearch elasticsearch

stop:
	docker stop elasticsearch