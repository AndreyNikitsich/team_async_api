from polyfactory.factories import TypedDictFactory

from ..models.related_to_film import RelatedToFilm
from ..settings import fake


class RelatedToFilmFactory(TypedDictFactory[RelatedToFilm]):
    __model__ = RelatedToFilm
    __faker__ = fake

    @classmethod
    def number_of_definitions(cls):
        numbers = [1, 2, 3, 4]
        number_weights = [0.5, 0.3, 0.15, 0.05]
        return cls.__faker__.random.choices(numbers, number_weights, k=1)[0]

    @classmethod
    def number_of_genres(cls):
        return cls.number_of_definitions()

    @classmethod
    def number_of_directors(cls):
        numbers = [1, 2, 3]
        number_weights = [0.7, 0.2, 0.1]
        return cls.__faker__.random.choices(numbers, number_weights, k=1)[0]

    @classmethod
    def number_of_actors(cls):
        numbers = [3, 4, 5, 6, 7]
        number_weights = [0.1, 0.2, 0.4, 0.2, 0.1]
        return cls.__faker__.random.choices(numbers, number_weights, k=1)[0]

    @classmethod
    def number_of_writers(cls):
        numbers = [1, 2, 3]
        number_weights = [0.1, 0.7, 0.2]
        return cls.__faker__.random.choices(numbers, number_weights, k=1)[0]
