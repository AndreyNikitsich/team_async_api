from polyfactory import Require
from polyfactory.factories import TypedDictFactory

from ..models.cover import Cover
from ..settings import fake
from .mixins import TimestampedMixin


class CoverFactory(TimestampedMixin, TypedDictFactory[Cover]):
    __model__ = Cover
    __faker__ = fake

    film_id = Require()
    size = Require()
    url = Require()
