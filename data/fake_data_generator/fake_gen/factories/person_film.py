from polyfactory import Require
from polyfactory.factories import TypedDictFactory

from .mixins import TimestampedMixin
from ..models.person_film import PersonFilm
from ..settings import fake


class PersonFilmFactory(TimestampedMixin, TypedDictFactory[PersonFilm]):
    __model__ = PersonFilm
    __faker__ = fake

    film_id = Require()
    person_id = Require()
    role = Require()
