from polyfactory import Require
from polyfactory.factories import TypedDictFactory

from .mixins import TimestampedMixin
from ..models.definition_film import DefinitionFilm
from ..settings import fake


class DefinitionFilmFactory(TimestampedMixin, TypedDictFactory[DefinitionFilm]):
    __model__ = DefinitionFilm
    __faker__ = fake

    definition_id = Require()
    film_id = Require()
