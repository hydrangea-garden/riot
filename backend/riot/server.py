from types import SimpleNamespace
from typing import Any

from riot.api.account import Account
from riot.api.league import League
from riot.api.wrapper import RiotAPI
from riot.config import ServerConfig
from sanic import Request, Sanic
from sanic.response import json

from backend.riot.api.summoner import Summoner


class ServerContext(SimpleNamespace):
    riot_api: RiotAPI


class Server(Sanic[ServerConfig, ServerContext]): ...


class ServerRequest(Request):
    app: Server
    args: property
    json: Any


async def setup_api(app: Server) -> None:
    app.ctx.riot_api = RiotAPI(api_key=app.config.RIOT_API_KEY)


async def get_info(request: ServerRequest):
    account = Account(request.app.ctx.riot_api)
    league = League(request.app.ctx.riot_api)
    summoner = Summoner(request.app.ctx.riot_api)
    response = await account.get_account_by_game_name_and_tag(
        game_name=request.json.get("game_name", ""),
        tag_line=request.json.get("tag_line", ""),
    )

    puuid = response["puuid"]

    if not response:
        return json({"error": "Account not found"}, status=404)

    summoner_info = await summoner.get_summoner_by_puuid(puuid=puuid)

    res = await league.get_league_entries_by_puuid(puuid=puuid)
    if not res:
        return json({"error": "League entries not found"}, status=404)

    return json(
        {
            "name": summoner_info["name"],
            "level": summoner_info["summonerLevel"],
            "iconId": summoner_info["profileIconId"],
            "tier": res[0]["tier"],
            "rank": res[0]["rank"],
            "leaguePoints": res[0]["leaguePoints"],
            "wins": res[0]["wins"],
            "losses": res[0]["losses"],
        }
    )


def create_app(config: ServerConfig) -> Server:
    app = Server("RiotAPIWrapper", config=config)
    app.add_route(get_info, "/info", methods=["POST"])
    app.before_server_start(setup_api)
    app.config.update(config)
    return app
