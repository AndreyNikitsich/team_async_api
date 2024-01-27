-- CREATE MOVIES DATABASE SCRIPT

CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS content.film (
  id uuid PRIMARY KEY,
  title VARCHAR (255) NOT NULL,
  imdb_rating FLOAT,
  mpaa_rating VARCHAR (5) NOT NULL,
  accessibility_features VARCHAR (5) [] NOT NULL DEFAULT '{}'::VARCHAR (5) [],
  duration_settings INT NOT NULL,
  release_date TIMESTAMP WITH TIME ZONE,
  description TEXT NOT NULL,

  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre (
  id uuid PRIMARY KEY,
  name VARCHAR (255) NOT NULL,
  description TEXT NOT NULL,

  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film (
  id uuid PRIMARY KEY,
  genre_id uuid NOT NULL,
  film_id uuid NOT NULL,

  created TIMESTAMP WITH TIME ZONE,

  CONSTRAINT fk_genre_id
    FOREIGN KEY (genre_id)
    REFERENCES content.genre (id)
    ON DELETE CASCADE,

  CONSTRAINT fk_film_id
    FOREIGN KEY (film_id)
    REFERENCES content.film (id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.cover (
  id uuid PRIMARY KEY,
  film_id uuid REFERENCES content.film (id) ON DELETE CASCADE,
  size VARCHAR (16) NOT NULL,
  url VARCHAR (256) NOT NULL,

  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.definition (
  id uuid PRIMARY KEY,
  name VARCHAR (256) UNIQUE NOT NULL,

  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.definition_film (
  id uuid PRIMARY KEY,
  definition_id uuid NOT NULL,
  film_id uuid NOT NULL,

  created TIMESTAMP WITH TIME ZONE,

  CONSTRAINT fk_definition_id
    FOREIGN KEY (definition_id)
    REFERENCES content.definition (id)
    ON DELETE CASCADE,

  CONSTRAINT fk_film_id
    FOREIGN KEY (film_id)
    REFERENCES content.film (id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.person (
  id uuid PRIMARY KEY,
  full_name VARCHAR(256),

  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person_film (
  id uuid PRIMARY KEY,
  person_id uuid NOT NULL,
  film_id uuid NOT NULL,
  role VARCHAR (64) NOT NULL,

  created TIMESTAMP WITH TIME ZONE,
  modified TIMESTAMP WITH TIME ZONE,

  CONSTRAINT fk_person_id
    FOREIGN KEY (person_id)
    REFERENCES content.person (id)
    ON DELETE CASCADE,

  CONSTRAINT fk_film_id
    FOREIGN KEY (film_id)
    REFERENCES content.film (id)
    ON DELETE CASCADE
);