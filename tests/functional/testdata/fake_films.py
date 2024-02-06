import random
from typing import Any

from faker import Faker
from faker.providers import DynamicProvider
from pydantic import BaseModel

persons_name_provider = DynamicProvider(
    provider_name="person_name",
    elements=["Stan", "Ann", "Bob", "Ben", "Howard"],
)

genres_name_provider = DynamicProvider(
    provider_name="genre_name",
    elements=["Action", "Sci-Fi", "Comedy"],
)

fake = Faker()

fake.add_provider(persons_name_provider)
fake.add_provider(genres_name_provider)


class FilmPerson(BaseModel):
    id: str
    name: str


class FilmGenre(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float
    title: str
    description: str

    genres: list[FilmGenre]
    genres_names: list[str]

    directors: list[FilmPerson]
    directors_names: list[str]

    actors: list[FilmPerson]
    actors_names: list[str]

    writers: list[FilmPerson]
    writers_names: list[str]


def generate_genres(cnt: int) -> list[FilmGenre]:
    """Генератор фейковых данных для жанров в фильме."""
    return [FilmGenre(
        id=fake.uuid4(),
        name=fake.genre_name()
    ) for _ in range(cnt)]


def generate_persons(cnt: int) -> list[FilmPerson]:
    """Генератор фейковых данных для персон в фильме."""
    return [FilmPerson(
        id=fake.uuid4(),
        name=fake.person_name()
    ) for _ in range(cnt)]


def generate_films(cnt: int) -> list[Film]:
    """Генератор фейковых данных фильмов."""
    genres = generate_genres(3)
    persons = generate_persons(5)
    return [Film(
        id=fake.uuid4(),
        imdb_rating=round(random.uniform(0, 10), 1),
        title="The Star",
        description=fake.paragraph(),
        genres=genres,
        genres_names=[genre.name for genre in genres],
        directors=persons[:1],
        directors_names=[person.name for person in persons[:1]],
        actors=persons[1:3],
        actors_names=[person.name for person in persons[1:3]],
        writers=persons[3:],
        writers_names=[person.name for person in persons[1:3]]
    ) for _ in range(cnt)]


def generate_film_by_id(film_id: str) -> Film:
    """
    Генератор фейковых данных одного фильма с предустановленным id,
    для тестирования вывода фильма по uuid.
    """
    genres = generate_genres(3)
    persons = generate_persons(5)
    return Film(
        id=film_id,
        imdb_rating=round(random.uniform(0, 10), 1),
        title="The Star",
        description=fake.paragraph(),
        genres=genres,
        genres_names=[genre.name for genre in genres],
        directors=persons[:1],
        directors_names=[person.name for person in persons[:1]],
        actors=persons[1:3],
        actors_names=[person.name for person in persons[1:3]],
        writers=persons[3:],
        writers_names=[person.name for person in persons[1:3]]
    )


def generate_films_data(
        cnt: int,
        constant_id: str = "72a42e8c-fdc4-42df-8da5-145907d6309b"
) -> list[dict[str, Any]]:
    """Генератор данных для загрузки в ЕС."""
    films = generate_films(cnt - 1)
    films.append(generate_film_by_id(constant_id))
    return [film.model_dump() for film in films]
