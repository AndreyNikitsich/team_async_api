import random
from enum import Enum
from typing import Any

from faker import Faker
from pydantic import BaseModel

fake = Faker()

person_names = [
    "Martin Anderson",
    "Nathan Stone",
    "John Cisneros",
    "Jeffrey Howell",
    "Brianna Aguirre",
    "Rebekah Wiggins",
    "Rebekah Allen",
    "Jennifer Davis",
    "Derrick Gomez",
    "Lindsey Davis",
    "Cristian Harris",
    "Jessica Wheeler",
    "Cheryl Ray",
    "Janice Harris",
    "Norman Gardner",
    "Diane Lewis",
    "Robert Wagner",
    "Gregory Baldwin",
    "Lisa Allen",
    "Nicole Vasquez",
    "Nicholas Robles",
    "Deborah Lucas",
    "Kaylee Taylor",
    "Gregory Patterson",
    "Lisa Moses",
    "Mike Duncan",
    "Matthew Holmes",
    "Jonathan Fowler",
    "John Peterson",
    "Jennifer Mcneil",
    "Robert Goodman",
    "John Barron",
    "Cody Turner",
    "Anthony Farrell",
    "Elizabeth Crawford",
    "Emma Hall",
    "Philip Boyd",
    "Robert Myers",
    "Lisa Lee",
    "Daniel Collins",
    "Sean Morgan",
    "Norma Flynn",
    "Michael Goodman",
    "Sarah Chavez",
    "Bradley Maldonado",
    "Stacy Carlson",
    "Tara Hernandez",
    "Antonio Smith",
    "Adam Mccoy",
    "Brian Scott",
    "Susan Gibson",
]


class PersonFilmRoles(str, Enum):
    WRITER = "writer"
    DIRECTOR = "director"
    ACTOR = "actor"


class PersonFilm(BaseModel):
    id: str
    title: str
    roles: list[PersonFilmRoles]


class Person(BaseModel):
    id: str
    full_name: str
    films: list[PersonFilm]


def generate_person_films(count: int) -> list[PersonFilm]:
    """Генератор фейковых фильмов для персоналий."""
    return [
        PersonFilm(
            id=fake.uuid4(), title=fake.paragraph(), roles=random.choices(list(PersonFilmRoles), k=random.randint(1, 3))
        )
        for _ in range(count)
    ]


def generate_persons() -> list[Person]:
    return [
        Person(id=fake.uuid4(), full_name=name, films=generate_person_films(random.randint(1, 5)))
        for name in person_names
    ]

generated_person_films = generate_person_films(5)

def generate_person_by_id(person_id: str) -> Person:
    """
    Генератор фейковых данных одной персоны с предустановленным id,
    для тестирования вывода персоны по uuid.
    """
    return Person(id=person_id, full_name="Lee Trump", films=generated_person_films)


def generate_persons_data(constant_id: str = "20f26754-95da-4a4e-98a5-ea78e3d29862") -> list[dict[str, Any]]:
    """Генератор данных для загрузки в ЕС."""
    persons = generate_persons()
    persons.append(generate_person_by_id(constant_id))
    return [person.model_dump() for person in persons]
