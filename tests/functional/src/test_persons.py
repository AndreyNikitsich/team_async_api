import pytest
from faker import Faker

from ..settings import test_settings

fake = Faker()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
                {
                    "query": "Lee",
                },
                {"status": 200, "length": 50}
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
