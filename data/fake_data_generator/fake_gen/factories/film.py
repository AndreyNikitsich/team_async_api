from datetime import datetime

from polyfactory.factories import TypedDictFactory

from ..models.film import Film
from ..settings import fake
from .mixins import TimestampedMixin


class FilmFactory(TimestampedMixin, TypedDictFactory[Film]):
    __model__ = Film
    __faker__ = fake

    _description_length = 500

    @classmethod
    def title(cls) -> str:
        number_of_words = cls.__faker__.random.randint(1, 4)
        words = cls.__faker__.words(number_of_words)
        return ' '.join(words).capitalize()

    @classmethod
    def imdb_rating(cls) -> float:
        return round(cls.__faker__.random.random() * 10, 2)

    @classmethod
    def release_date(cls) -> datetime:
        return cls.__faker__.date_between('-40y', 'today')

    @classmethod
    def description(cls) -> str:
        return cls.__faker__.text(cls._description_length)
