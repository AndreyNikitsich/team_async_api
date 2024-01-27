-- DESTROY MOVIES DATABASE SCRIPT

DROP TABLE IF EXISTS content.person_film;
DROP TABLE IF EXISTS content.person;
DROP TABLE IF EXISTS content.definition_film;
DROP TABLE IF EXISTS content.definition;
DROP TABLE IF EXISTS content.cover;
DROP TABLE IF EXISTS content.genre_film;
DROP TABLE IF EXISTS content.genre;
DROP TABLE IF EXISTS content.film;

ALTER ROLE app SET search_path TO "$user", public;

DROP SCHEMA IF EXISTS content;