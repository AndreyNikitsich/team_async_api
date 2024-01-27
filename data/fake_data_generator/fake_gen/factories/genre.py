from polyfactory.factories import TypedDictFactory

from ..models.genre import Genre
from ..settings import fake
from .mixins import TimestampedMixin


class GenreFactory(TimestampedMixin, TypedDictFactory[Genre]):
    __model__ = Genre
    __faker__ = fake

    _description_length = 500

    @classmethod
    def name(cls) -> str:
        return cls.__faker__.genre()

    @classmethod
    def description(cls) -> str:
        return cls.__faker__.text(cls._description_length)
