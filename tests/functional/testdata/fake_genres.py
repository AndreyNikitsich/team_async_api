from typing import Any

from faker import Faker
from faker.providers import DynamicProvider
from pydantic import BaseModel

genre_names = [
    "Anime",
    "Biographical",
    "Action movie",
    "Western film",
    "Military",
    "Detective",
    "Childish",
    "Documentary",
    "Drama",
    "Historical",
    "Movie comic",
    "Comedy",
    "Concert",
    "Short",
    "Crime",
    "Melodrama",
    "Mystic",
    "Music",
    "Cartoon",
    "Musical",
    "Scientific",
    "Noir",
    "Adventures",
    "Reality show",
    "Family",
    "Sport",
    "Talk show",
    "Thriller",
    "Horror",
]

genres_name_provider = DynamicProvider(
    provider_name="genre_name",
    elements=genre_names,
)

fake = Faker()

fake.add_provider(genres_name_provider)


class Genre(BaseModel):
    id: str
    name: str
    description: str


def generate_genres() -> list[Genre]:
    """Генератор фейковых данных для жанров."""
    return [Genre(
        id=fake.uuid4(),
        name=name,
        description=fake.paragraph()
    ) for name in genre_names]


def generate_genre_by_id(genre_id: str) -> Genre:
    """
    Генератор фейковых данных одного жанра с предустановленным id,
    для тестирования вывода жанра по uuid.
    """
    return Genre(
        id=genre_id,
        name="Fantastic",
        description=fake.paragraph()
    )


def generate_genres_data(
        constant_id: str = "08952b1c-55ff-4cc4-8078-b37fc41b6ff5"
) -> list[dict[str, Any]]:
    """Генератор данных для загрузки в ЕС."""
    genres = generate_genres()
    genres.append(generate_genre_by_id(constant_id))
    return [genre.model_dump() for genre in genres]
