import pytest
import pytest_asyncio

from functional.settings import film_settings
from functional.testdata import fake_films
from functional.utils.es_index import ESIndex


@pytest.fixture(scope="module", name="films_data")
def films_data():
    es_data = fake_films.generate_films_data(60)

    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": "movies", "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    return bulk_query


@pytest.fixture(scope="module")
def film_index(es_client):
    return ESIndex(
        client=es_client,
        test_config=film_settings
    )


@pytest_asyncio.fixture(scope="module", name="prepare_films_data")
async def prepare_films_data(film_index, films_data):
    await film_index.create()
    await film_index.update(films_data)

    yield

    await film_index.delete()
