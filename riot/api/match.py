from riot.api.route import Route
from riot.api.wrapper import RiotAPI, T


class Match:
    MATCH_PATH = "/lol/match/v5/matches"

    def __inot__(self, api: RiotAPI):
        self.api = api

    def get_match_route(self, method: str, path: str, type: type[T]):
        return Route(
            method=method,
            path=self.MATCH_PATH + path,
            response_type=type,
            region="asia",
        )

    async def get_match_ids(self, puuid: str):
        # currently, this method fetches the last 10 match IDs for a given PUUID
        return await self.api.fetch(
            self.get_match_route("GET", f"/by-puuid/{puuid}/ids?count=10", list[str])
        )
