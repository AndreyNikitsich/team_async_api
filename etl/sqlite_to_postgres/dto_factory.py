from dto import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class ObjectFactory:
    def __init__(self):
        self._objects = {}

    def register(self, key, object_):
        self._objects[key] = object_

    def create(self, key, **kwargs):
        object_ = self._objects.get(key)
        if not object_:
            raise ValueError(key)
        return object_(**kwargs)

    def is_register(self, key):
        return key in self._objects

    def registered(self):
        return self._objects


factory = ObjectFactory()

factory.register("film_work", FilmWork)
factory.register("genre", Genre)
factory.register("person", Person)
factory.register("genre_film_work", GenreFilmWork)
factory.register("person_film_work", PersonFilmWork)
