CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);


CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    genre_id     uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created      timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    person_id    uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role         TEXT,
    created      timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work (creation_date);
CREATE INDEX IF NOT EXISTS film_work_title_idx ON content.film_work (title);

ALTER TABLE content.genre_film_work DROP CONSTRAINT IF EXISTS unique_film_work_genre;
ALTER TABLE content.genre_film_work ADD CONSTRAINT unique_film_work_genre UNIQUE (film_work_id, genre_id);

ALTER TABLE content.person_film_work DROP CONSTRAINT IF EXISTS unique_film_work_person_role;
ALTER TABLE content.person_film_work ADD CONSTRAINT unique_film_work_person_role UNIQUE (film_work_id, person_id, role);
