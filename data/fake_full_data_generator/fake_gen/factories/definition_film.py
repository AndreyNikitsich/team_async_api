from polyfactory import Require
from polyfactory.factories import TypedDictFactory

from ..models.definition_film import DefinitionFilm
from ..settings import fake
from .mixins import TimestampedMixin


class DefinitionFilmFactory(TimestampedMixin, TypedDictFactory[DefinitionFilm]):
    __model__ = DefinitionFilm
    __faker__ = fake

    definition_id = Require()
    film_id = Require()
