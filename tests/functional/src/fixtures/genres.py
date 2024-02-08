import pytest
import pytest_asyncio

from functional.settings import genre_settings
from functional.testdata import fake_genres
from functional.utils.es_index import ESIndex


@pytest.fixture(scope="module", name="genres_data")
def genres_data():
    es_data = fake_genres.generate_genres_data()

    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": genre_settings.ES_INDEX, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    return bulk_query


@pytest.fixture(scope="module")
def genre_index(es_client):
    return ESIndex(
        client=es_client,
        test_config=genre_settings
    )


@pytest_asyncio.fixture(scope="module", name="prepare_genres_data")
async def prepare_genres_data(genre_index, genres_data):
    await genre_index.delete()
    await genre_index.create()
    await genre_index.update(genres_data)
