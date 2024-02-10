build:
	docker build -t load_data:latest .

run:
	docker run --rm -it --name load_data --net=movies_admin_backend --env-file .\.env load_data
	python ./load_data.py && exit

stop:
	docker stop load_data
	docker rm load_data
