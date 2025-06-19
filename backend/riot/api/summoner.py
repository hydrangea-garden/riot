from typing import TypedDict

from riot.api.route import Route
from riot.api.wrapper import RiotAPI, T


class SummonerDTO(TypedDict):
    puuid: str
    name: str
    profileIconId: int
    revisionDate: int
    summonerLevel: int


class Summoner:
    SUMMONER_PATH = "/lol/summoner/v4/summoners"

    def __init__(self, api: RiotAPI):
        self.api = api

    def get_summoner_route(self, method: str, path: str, type: type[T]):
        return Route(
            method=method,
            path=self.SUMMONER_PATH + path,
            response_type=type,
            region="kr",
        )

    async def get_summoner_by_puuid(self, puuid: str):
        return await self.api.fetch(
            self.get_summoner_route("GET", f"/by-puuid/{puuid}", SummonerDTO)
        )
