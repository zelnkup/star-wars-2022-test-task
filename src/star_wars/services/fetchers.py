import abc
import asyncio
from math import ceil

from src.integrations.sw_api.client import ClientMode, ResourceType, StarWarsClient

__all__ = ("GetCharactersService", "GetPlanetsService")


class GetItemsMixin:
    """
    Mixin for fetching data from SW API using async requests
    with self counted pages quantity
    """

    resource: ResourceType

    def count_items_pages(self) -> int:
        response = StarWarsClient({"page": 1}, resource=self.resource).get_items()
        return ceil(response["count"] / len(response["results"]))

    @property
    def pages_count(self) -> int:
        return self.count_items_pages()

    @abc.abstractmethod
    def get_items(self):
        raise NotImplementedError()


class GetCharactersService(GetItemsMixin):
    """
    Service for getting all characters from Star Wars API
    using async requests
    """

    resource = ResourceType.CHARACTERS

    async def get_items(self):
        tasks = [
            StarWarsClient(
                {"page": page}, mode=ClientMode.ASYNC, resource=self.resource
            ).get_items()
            for page in range(1, self.pages_count + 1)
        ]

        return await asyncio.gather(*tasks)


class GetPlanetsService(GetItemsMixin):
    """
    Service for getting all planets from Star Wars API
    using async requests
    """

    resource = ResourceType.PLANETS

    async def get_items(self):
        tasks = [
            StarWarsClient(
                {"page": page}, mode=ClientMode.ASYNC, resource=self.resource
            ).get_items()
            for page in range(1, self.pages_count + 1)
        ]

        return await asyncio.gather(*tasks)
