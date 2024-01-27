from itertools import combinations
from typing import Generator

from faker.providers import BaseProvider


class GenreProvider(BaseProvider):
    genres_collection = [
        'аниме',
        'биографический',
        'боевик',
        'вестерн',
        'военный',
        'детектив',
        'детский',
        'документальный',
        'драма',
        'исторический',
        'кинокомикс',
        'комедия',
        'концерт',
        'короткометражный',
        'криминал',
        'мелодрама',
        'мистика',
        'музыка',
        'мультфильм',
        'мюзикл',
        'научный',
        'нуар',
        'приключения',
        'реалити-шоу',
        'семейный',
        'спорт',
        'ток-шоу',
        'триллер',
        'ужасы',
        'фантастика',
        'фэнтези',
        # 'эротика',
    ]

    def __init__(self, generator):
        super().__init__(generator)
        self._all_genres = self.genres_collection
        self._genres = self._infinite_genre_generator()

    def set_number_of_unique_genres(self, number_of_unique: int):
        genre_generator = self._infinite_unique_genre_generator()
        self._all_genres = [next(genre_generator) for _ in range(number_of_unique)]
        self._genres = self._infinite_genre_generator()

    def genre(self) -> str:
        return next(self._genres)

    def _infinite_genre_generator(self) -> Generator[str, None, None]:
        yield from self._all_genres
        while True:  # noqa: WPS457
            yield self.generator.random.choice(self._all_genres)  # noqa: S311

    def _infinite_unique_genre_generator(self) -> Generator[str, None, None]:
        genres_collection = self.genres_collection
        yield from genres_collection
        words_count = 2
        while True:  # noqa: WPS457
            yield from (
                ''.join(words)
                for words in combinations(genres_collection, words_count)
            )
            words_count += 1
