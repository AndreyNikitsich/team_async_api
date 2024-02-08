import pytest
from faker import Faker

from ..settings import test_settings

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "page_number": 1,
                    "page_size": 50,
                },
                {"status": 200, "length": 30}
        ),
        (
                {
                    "page_size": 50,
                },
                {"status": 200, "length": 30}
        ),
        (
                {
                    "page_number": 1,
                },
                {"status": 200, "length": 30}
        ),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_genres_data")
async def test_genres(make_get_request, query_data, expected_answer):
    """Список жанров."""
    url = test_settings.SERVICE_URL + "/api/v1/genres"
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
@pytest.mark.usefixtures("prepare_films_data")
async def test_genre_by_uuid(make_get_request, uuid, expected_status):
    """Вывод конкретного жанра."""
    url = test_settings.SERVICE_URL + "/api/v1/genres/" + uuid
    body, headers, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        (fake.uuid4(), 404),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_genre_not_found_by_uuid(make_get_request, uuid, expected_status):
    """Вывод несуществующего жанра."""
    url = test_settings.SERVICE_URL + "/api/v1/genres/" + uuid
    body, headers, status = await make_get_request(url)

    assert status == expected_status


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        ("08952b1c-55ff-4cc4-8078-b37fc41b6ff5", 200),
    ]
)
@pytest.mark.asyncio
async def test_film_by_uuid_from_cache(make_get_request, uuid, expected_status):
    """Вывод жанра с учетом кеша."""
    url = test_settings.SERVICE_URL + "/api/v1/genres/" + uuid
    body, headers, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid
