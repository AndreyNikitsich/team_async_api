from polyfactory import Require
from polyfactory.factories import TypedDictFactory

from ..models.person_film import PersonFilm
from ..settings import fake
from .mixins import TimestampedMixin


class PersonFilmFactory(TimestampedMixin, TypedDictFactory[PersonFilm]):
    __model__ = PersonFilm
    __faker__ = fake

    film_id = Require()
    person_id = Require()
    role = Require()
