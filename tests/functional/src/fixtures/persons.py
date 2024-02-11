import pytest
import pytest_asyncio
from functional.settings import person_settings
from functional.testdata import fake_persons
from functional.utils.es_index import ESIndex


@pytest.fixture(scope="module", name="persons_data")
def persons_data():
    es_data = fake_persons.generate_persons_data()

    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": person_settings.es_index, "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)

    return bulk_query


@pytest.fixture(scope="module")
def person_index(es_client):
    return ESIndex(
        client=es_client,
        test_config=person_settings
    )


@pytest_asyncio.fixture(scope="module", name="prepare_persons_data")
async def prepare_persons_data(person_index, persons_data):
    await person_index.delete()
    await person_index.create()
    await person_index.update(persons_data)
