from datetime import datetime

from polyfactory.factories import TypedDictFactory

from ..models.accessibility import Accessibility
from ..models.film import Film
from ..models.mpaa_rating import MPAARating
from ..settings import fake
from .mixins import TimestampedMixin


class FilmFactory(TimestampedMixin, TypedDictFactory[Film]):
    __model__ = Film
    __faker__ = fake

    _duration_range = (1200, 7200)
    _description_length = 2000

    @classmethod
    def title(cls) -> str:
        number_of_words = cls.__faker__.random.randint(1, 4)
        words = cls.__faker__.words(number_of_words)
        return ' '.join(words).capitalize()

    @classmethod
    def imdb_rating(cls) -> float:
        return round(cls.__faker__.random.random() * 10, 2)

    @classmethod
    def mpaa_rating(cls) -> MPAARating:
        return cls.__faker__.mpaa_rating()

    @classmethod
    def accessibility_features(cls) -> list[Accessibility]:
        return cls.__faker__.accessibility()

    @classmethod
    def duration_seconds(cls) -> int:
        return cls.__faker__.random.randint(*cls._duration_range)

    @classmethod
    def release_date(cls) -> datetime:
        return cls.__faker__.date_between('-40y', 'today')

    @classmethod
    def description(cls) -> str:
        return cls.__faker__.text(cls._description_length)
