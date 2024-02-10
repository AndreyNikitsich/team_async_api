import pytest
from faker import Faker

from functional.testdata.fake_persons import generated_person_films

from ..settings import test_settings

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "query": "Rebekah Wiggins",
                },
                {"status": 200, "length": 1}
        ),
        (
                {
                    "query": "NOT_FOUNDED_NAME",
                },
                {"status": 200, "length": 0}
        ),
        (
                {
                    "query": "Rebecah Wigins",  # test full text search, should find "Rebekah Wiggins"
                },
                {"status": 200, "length": 1}
        ),
        (
                {
                    "query": "Rebekah",  # test full text search, should find "Rebekah Wiggins", "Rebekah Allen"
                },
                {"status": 200, "length": 2}
        ),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_persons_data")
async def test_persons_search(make_get_request, query_data, expected_answer):
    """Поиск персон."""
    url = test_settings.SERVICE_URL + "/api/v1/persons/search"
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        ("08952b1c-55ff-4cc4-8078-b37fc41b6ff5", 200),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_persons_data")
async def test_person_detail(make_get_request, uuid, expected_status):
    """Вывод информации о конкретной персоне."""
    url = test_settings.SERVICE_URL + "/api/v1/persons/" + uuid
    body, headers, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        ("08952b1c-55ff-4cc4-8078-b37fc41b6ff5", 200),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_persons_data")
async def test_persons_films(make_get_request, uuid, expected_status):
    """Проверка списка фильмов, в которых принимала участие персона."""
    url = test_settings.SERVICE_URL + f"/api/v1/persons/{uuid}/films"
    body, headers, status = await make_get_request(url)

    assert status == expected_status
    assert len(generated_person_films) == len(body)
