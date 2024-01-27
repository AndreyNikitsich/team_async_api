from polyfactory.factories import TypedDictFactory

from ..models.person import Person
from ..settings import fake
from .mixins import TimestampedMixin


class PersonFactory(TimestampedMixin, TypedDictFactory[Person]):
    __model__ = Person
    __faker__ = fake

    @classmethod
    def full_name(cls) -> str:
        name = cls.__faker__.name().split()
        return ' '.join(name[:2])
