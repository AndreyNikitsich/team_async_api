import random
from enum import Enum
from typing import Any

from faker import Faker
from faker.providers import DynamicProvider
from pydantic import BaseModel

fake = Faker()

person_names = ['Cheryl', 'William', 'David', 'Rhonda', 'Nicole', 'Jennifer', 'Tina', 'Denise', 'Elizabeth', 'Edward',
                'Jeremy', 'Ian', 'Logan', 'Kristin', 'Mary', 'Shawn', 'Raymond', 'Kimberly', 'Kendra', 'Heather',
                'Anthony', 'Cynthia', 'Paul', 'Karen', 'Randall', 'Julie', 'Keith', 'Steven', 'Evan', 'Nancy',
                'Maureen', 'Alexander', 'Brandon', 'Dawn', 'Charlene', 'Anita', 'Jeffrey', 'Mercedes',
                'Marissa', 'Allison', 'Shirley', 'Jose', 'Kyle', 'Maria', 'Julia', 'Kathleen', 'Diana', 'Juan', 'Jimmy']

persons_name_provider = DynamicProvider(
    provider_name="person_name",
    elements=person_names,
)
fake.add_provider(persons_name_provider)


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
            id=fake.uuid4(),
            title=fake.paragraph(),
            roles=random.choices(list(PersonFilmRoles), k=random.randint(1, 3))
        )
        for _ in range(count)
    ]


def generate_persons() -> list[Person]:
    return [
        Person(
            id=fake.uuid4(),
            full_name=name,
            films=generate_person_films(random.randint(1, 5))
        )
        for name in person_names
    ]


def generate_person_by_id(person_id: str) -> Person:
    """
    Генератор фейковых данных одной персоны с предустановленным id,
    для тестирования вывода персоны по uuid.
    """
    return Person(
        id=person_id,
        full_name="Lee",
        films=generate_person_films(random.randint(1, 5))
    )


def generate_persons_data(
        constant_id: str = "08952b1c-55ff-4cc4-8078-b37fc41b6ff5"
) -> list[dict[str, Any]]:
    """Генератор данных для загрузки в ЕС."""
    persons = []
    persons.append(generate_person_by_id(constant_id))
    return [person.model_dump() for person in persons]
