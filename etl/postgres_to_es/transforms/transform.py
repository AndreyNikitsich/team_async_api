from typing import Any

from transforms.models import genres, movies, persons

es_models = {
    "movies": movies.ESMovie,
    "genres": genres.ESGenre,
    "persons": persons.ESPerson
}


class DataTransform:
    @staticmethod
    def transform(
            data: tuple[str, list[dict[str, Any]]]
    ) -> tuple[str, list[dict[str, Any]]]:
        es_data = []
        index, rows = data
        for row in rows:
            es_model = es_models[index](**row)
            es_data.append(es_model.model_dump(by_alias=True))
        return index, es_data
