-- CREATE MOVIES DATABASE SCRIPT

CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS content.film
(
    id uuid PRIMARY KEY,
    title VARCHAR (255) NOT NULL ,
    description TEXT,
    release_date DATE,
    imdb_rating FLOAT,

    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre
(
    id uuid PRIMARY KEY ,
    name VARCHAR (64) NOT NULL ,
    description TEXT,

    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person
(
    id uuid PRIMARY KEY ,
    full_name VARCHAR (255) NOT NULL ,

    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film
(
    id uuid PRIMARY KEY ,
    genre_id uuid NOT NULL ,
    film_id uuid NOT NULL ,

    created TIMESTAMP WITH TIME ZONE,

    CONSTRAINT fk_genre_id
        FOREIGN KEY (genre_id)
        REFERENCES content.genre (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.person_film
(
    id uuid PRIMARY KEY ,
    person_id uuid NOT NULL ,
    film_id uuid NOT NULL ,
    role varchar (255) NOT NULL ,

    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE,

    CONSTRAINT fk_person_id
        FOREIGN KEY (person_id)
        REFERENCES content.person (id)
        ON DELETE CASCADE
);
