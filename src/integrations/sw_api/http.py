from dataclasses import dataclass

import httpx

from src.integrations.sw_api.exceptions import StarWarsAPIHTTPException

__all__ = ("StarWarsAPIHTTP",)


@dataclass
class StarWarsAPIHTTP:
    """
    HTTP client for fetching data from SW API in async and sync modes using httpx library
    """

    timeout = httpx.Timeout(10.0, read=None)

    async def async_get(self, url, params=None):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=self.timeout)
            if response.status_code != 200:
                raise StarWarsAPIHTTPException(
                    f"Non-ok HTTP response from SW api: {response.json()}"
                )

        return response.json()["results"]

    def get(self, url, params=None):
        response = httpx.get(
            url,
            timeout=self.timeout,
            params=params,
        )
        if response.status_code != 200:
            raise StarWarsAPIHTTPException(
                f"Non-ok HTTP response from SW api: {response.json()}"
            )

        return response.json()
