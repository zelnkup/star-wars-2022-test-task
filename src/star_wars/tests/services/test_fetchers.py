from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.star_wars.services.fetchers import GetCharactersService, GetPlanetsService
from src.star_wars.tests.helpers import (
    mocked_sw_api_with_people,
    mocked_sw_api_with_planets,
)


@pytest.mark.asyncio
async def test_fetch_items_pages_count():
    with patch(
        "src.star_wars.services.fetchers.GetPlanetsService",
    ) as mocked_fetcher:
        mocked_fetcher.pages_count = 3
        with patch(
            "src.integrations.sw_api.client.StarWarsClient.get_items"
        ) as mocked_client:
            await GetPlanetsService().get_items()

    assert mocked_client.call_count == 1


@pytest.mark.asyncio
@patch(
    "src.star_wars.services.fetchers.GetPlanetsService.count_items_pages",
    Mock(return_value=1),
)
@patch(
    "src.integrations.sw_api.client.StarWarsClient.get_items",
    AsyncMock(return_value=mocked_sw_api_with_planets()),
)
async def test_fetch_planets_ok():
    response = await GetPlanetsService().get_items()

    assert response[0]["count"] == 60
    assert response[0]["results"][0]["name"] == "Tatooine"


@pytest.mark.asyncio
@patch(
    "src.star_wars.services.fetchers.GetCharactersService.count_items_pages",
    Mock(return_value=1),
)
@patch(
    "src.integrations.sw_api.client.StarWarsClient.get_items",
    AsyncMock(return_value=mocked_sw_api_with_people()),
)
async def test_fetch_people_ok():
    response = await GetCharactersService().get_items()

    assert response[0]["count"] == 82
    assert response[0]["results"][0]["name"] == "Luke Skywalker"
