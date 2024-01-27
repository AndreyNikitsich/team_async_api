from polyfactory import Require
from polyfactory.factories import TypedDictFactory

from ..models.genre_film import GenreFilm
from ..settings import fake
from .mixins import TimestampedMixin


class GenreFilmFactory(TimestampedMixin, TypedDictFactory[GenreFilm]):
    __model__ = GenreFilm
    __faker__ = fake

    film_id = Require()
    genre_id = Require()
