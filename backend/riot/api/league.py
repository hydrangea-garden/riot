from typing import TypedDict

from riot.api.route import Route
from riot.api.wrapper import RiotAPI, T


class LeagueEntryDTO(TypedDict):
    leagueId: str
    queueType: str
    tier: str
    rank: str
    summonerId: str
    summonerName: str
    leaguePoints: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    freshBlood: bool
    hotStreak: bool


class League:
    LEAGUE_PATH = "/lol/league/v4"

    def __init__(self, api: RiotAPI):
        self.api = api

    def get_league_route(self, method: str, path: str, type: type[T]):
        return Route(
            method=method,
            path=self.LEAGUE_PATH + path,
            response_type=type,
            region="kr",
        )

    async def get_league_entries_by_puuid(self, puuid: str):
        return await self.api.fetch(
            self.get_league_route(
                "GET", f"/entries/by-puuid/{puuid}", list[LeagueEntryDTO]
            )
        )
