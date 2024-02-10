from pydantic import BaseModel


class ESPersonFilms(BaseModel):
    """
    Модель данных фильмов в которых присутствуют персоны с ролями в этих
    фильмах для индексации в Elasticsearch.
    """

    id: str
    title: str
    roles: list[str]


class ESPerson(BaseModel):
    """Модель данных персон для индексации в Elasticsearch."""

    id: str
    full_name: str
    films: list[ESPersonFilms]
