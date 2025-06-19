from typing import TypedDict

from riot.api.route import Route
from riot.api.wrapper import RiotAPI, T


class AccountDTO(TypedDict):
    puuid: str
    gameName: str
    tagLine: str


class Account:
    ACCOUNT_PATH = "/riot/account/v1/accounts"

    def __init__(self, api: RiotAPI):
        self.api = api

    def get_account_route(self, method: str, path: str, type: type[T]):
        return Route(
            method=method,
            path=self.ACCOUNT_PATH + path,
            response_type=type,
            region="asia",
        )

    async def get_account_by_game_name_and_tag(self, game_name: str, tag_line: str):
        return await self.api.fetch(
            self.get_account_route(
                "GET", f"/by-riot-id/{game_name}/{tag_line}", AccountDTO
            )
        )
