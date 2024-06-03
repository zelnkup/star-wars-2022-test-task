from dataclasses import dataclass
from itertools import chain

from src.star_wars.models import HomeWorld


@dataclass
class GetPlanetsMap:
    """
    Service for getting planets map from HomeWorld model or creating it from list of planets
    """

    instance: HomeWorld | list

    def __call__(self):
        match self.instance:
            case HomeWorld():
                return self.instance.homeworld_map
            case list():
                return self._create_map()

    def _create_map(self):
        return HomeWorld.objects.create(
            homeworld_map={
                planet["url"]: planet["name"]
                for planet in list(chain.from_iterable(self.instance))
            }
        ).homeworld_map
