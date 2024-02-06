import pytest
from faker import Faker

from ..settings import test_settings

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "query": "The Star",
                    "page_number": 1,
                    "page_size": 50,
                    "sort": "-imdb_rating"
                },
                {"status": 200, "length": 50}
        ),
        (
                {
                    "query": "Mashed potato",
                    "page_number": 1,
                    "page_size": 50,
                    "sort": "-imdb_rating"
                },
                {"status": 200, "length": 0}
        )
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_films_search(make_get_request, query_data, expected_answer):
    """Поиск фильмов."""
    url = test_settings.SERVICE_URL + "/api/v1/films/search"
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "page_number": 1,
                    "page_size": 50,
                    "sort": "-imdb_rating"
                },
                {"status": 200, "length": 50}
        ),
        (
                {
                    "page_number": 1,
                    "page_size": 50,
                    "sort": "-imdb_rating",
                    "genre": "Fake"
                },
                {"status": 200, "length": 0}
        ),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_films(make_get_request, query_data, expected_answer):
    """Список фильмов."""
    url = test_settings.SERVICE_URL + "/api/v1/films"
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "page_number": 1,
                    "page_size": 50,
                    "sort": "-imdb_rating",
                    "genre": "Action"
                },
                {"status": 200}
        ),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_films_genre(make_get_request, query_data, expected_answer):
    """Список фильмов с фильтрацией по жанрам."""
    url = test_settings.SERVICE_URL + "/api/v1/films"
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        ("72a42e8c-fdc4-42df-8da5-145907d6309b", 200),
    ]
)
@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_films_data")
async def test_film_by_uuid(make_get_request, uuid, expected_status):
    """Вывод конкретного фильма."""
    url = test_settings.SERVICE_URL + "/api/v1/films/" + uuid
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
async def test_film_not_found_by_uuid(make_get_request, uuid, expected_status):
    """Вывод несуществующего фильма."""
    url = test_settings.SERVICE_URL + "/api/v1/films/" + uuid
    body, headers, status = await make_get_request(url)

    assert status == expected_status


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "query": "The Star",
                    "page_number": 1,
                    "page_size": 50,
                    "sort": "-imdb_rating"
                },
                {"status": 200, "length": 50}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_from_cache(make_get_request, query_data, expected_answer):
    """Поиск фильмов с учетом кеша."""
    url = test_settings.SERVICE_URL + "/api/v1/films/search"
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer["status"]
    assert len(body) == expected_answer["length"]


@pytest.mark.parametrize(
    "uuid, expected_status",
    [
        ("72a42e8c-fdc4-42df-8da5-145907d6309b", 200),
    ]
)
@pytest.mark.asyncio
async def test_film_by_uuid_from_cache(make_get_request, uuid, expected_status):
    """Вывод фильма с учетом кеша."""
    url = test_settings.SERVICE_URL + "/api/v1/films/" + uuid
    body, headers, status = await make_get_request(url)

    assert status == expected_status
    assert body["uuid"] == uuid
