import pytest

from src.star_wars.services.planets import GetPlanetsMap
from src.star_wars.tests.helpers import get_homeworld_map, get_sw_api_planets_response


@pytest.mark.django_db
def test_get_planets_map_object_exists(homeworld_map_factory):
    homeworld_map = GetPlanetsMap(homeworld_map_factory)()

    assert homeworld_map == homeworld_map_factory.homeworld_map


@pytest.mark.django_db
def test_get_planets_map_object_does_not_exist():
    homeworld_map = GetPlanetsMap([get_sw_api_planets_response()])()

    assert homeworld_map == get_homeworld_map()
