from dataclasses import dataclass
from enum import Enum
from typing import Optional

from django.conf import settings

from src.integrations.sw_api.http import StarWarsAPIHTTP


class ClientMode(Enum):
    ASYNC = "async"
    SYNC = "sync"


class ResourceType(Enum):
    CHARACTERS = "people/"
    PLANETS = "planets/"


@dataclass
class StarWarsClient:
    """
    Client for fetching data from SW API
    Could for both in sync and async modes
    Based on resource type adjusts url and fetch proper resource
    Usage:
    StarWarsClient({"page": 1}, mode=ClientMode.ASYNC, resource=ResourceType.CHARACTERS).get_items()
    StarWarsClient({"page": 2}, resource=ResourceType.PLANETS).get_items()
    """

    params: Optional[dict]
    resource: ResourceType
    mode: ClientMode = ClientMode.SYNC
    base_url: str = settings.SW_API_URL
    http = StarWarsAPIHTTP()

    def get_items(self):
        url = self.base_url + self.resource.value
        match self.mode:
            case ClientMode.SYNC:
                return self.http.get(url, self.params)
            case ClientMode.ASYNC:
                return self.http.async_get(url, self.params)
