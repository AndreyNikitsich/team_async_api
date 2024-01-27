FROM postgres:16.1-alpine3.19
COPY create_tables.sql /docker-entrypoint-initdb.d/
CMD ["postgres"]
