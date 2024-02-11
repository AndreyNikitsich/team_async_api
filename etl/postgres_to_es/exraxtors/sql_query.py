# noinspection SqlAggregates
movies = """
SELECT
    fw.id,
    fw.rating,
    fw.title,
    fw.description,
    COALESCE(json_agg(DISTINCT g.name),'[]') as genres,
    COALESCE(
       json_agg(
           DISTINCT p.full_name
       ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
       '[]'
    ) as director_names,
    COALESCE(
       json_agg(
           DISTINCT p.full_name
       ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
       '[]'
    ) as actor_names,
    COALESCE(
       json_agg(
            DISTINCT p.full_name
       ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
       '[]'
    ) as writer_names,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
               'person_id', p.id,
               'person_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
        '[]'
    ) as actor,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
               'person_id', p.id,
               'person_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
        '[]'
    ) as writer
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > %s OR p.modified > %s OR g.modified > %s
GROUP BY fw.id
ORDER BY fw.modified DESC;
"""

genres = """
SELECT g.id,
       g.name,
       g.description
FROM content.genre g
WHERE g.modified > %s
"""

persons = """
WITH film_roles as (
    SELECT
        fw.id,
        fw.title,
        fw.rating,
        array_agg(pfw.role) as roles,
        pfw.person_id
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw on fw.id = pfw.film_work_id
        GROUP BY fw.id, pfw.person_id
)
SELECT
    p.id,
    p.full_name,
    COALESCE(
        json_agg(
            DISTINCT jsonb_build_object(
                'id', fr.id,
                'title', fr.title,
                'roles', fr.roles
            )
        ), '[]'
    ) as films
FROM content.person p
LEFT JOIN film_roles fr on fr.person_id = p.id
WHERE p.modified > %s
GROUP BY p.id;
"""
