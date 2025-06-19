from typing import TypeVar

import aiohttp

from riot.api.route import Route

T = TypeVar("T")


class RiotAPI:
    def __init__(self, api_key: str, session: aiohttp.ClientSession | None = None):
        self._api_key = api_key
        self.session = session
        if self.session:
            self.session.headers.update({"X-Riot-Token": self._api_key})

    async def fetch(self, route: Route[T]) -> T:
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={"X-Riot-Token": self._api_key}
            )
        async with self.session.request(
            route.method,
            route.url,
        ) as response:
            if response.status != 200:
                raise Exception(f"Error fetching data: {response.status}")
            return await response.json()
