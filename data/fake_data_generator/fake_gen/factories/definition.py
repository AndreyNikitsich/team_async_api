from typing import Generator

from polyfactory.factories import TypedDictFactory

from .mixins import TimestampedMixin
from ..models.definition import Definition
from ..providers.definitions import DefinitionProvider
from ..settings import fake

DEFINITIONS_COLLECTION = DefinitionProvider.definitions_collection
DEFINITIONS_COLLECTION_LEN = len(DEFINITIONS_COLLECTION)


def gen_definition() -> Generator[str, None, None]:
    yield from DEFINITIONS_COLLECTION


class DefinitionFactory(TimestampedMixin, TypedDictFactory[Definition]):
    __model__ = Definition
    __faker__ = fake

    _definitions_generator = gen_definition()

    @classmethod
    def name(cls):
        return next(cls._definitions_generator)
