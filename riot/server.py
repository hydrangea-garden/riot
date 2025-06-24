from types import SimpleNamespace
from typing import Any, Mapping, Sequence

from sanic import Request, Sanic
from sanic.response import json

from riot.api.account import Account
from riot.api.league import League
from riot.api.summoner import Summoner
from riot.api.wrapper import RiotAPI
from riot.config import ServerConfig


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
    try:
        response = await account.get_account_by_game_name_and_tag(
            game_name=request.json.get("game_name", ""),
            tag_line=request.json.get("tag_line", ""),
        )
    except Exception:
        return json({"error": "계정을 찾을 수 없습니다."}, status=404)

    puuid = response["puuid"]

    try:
        summoner_info = await summoner.get_summoner_by_puuid(puuid=puuid)
    except Exception:
        return json({"error": "소환사를 찾을 수 없습니다."}, status=404)

    res: Sequence[Mapping[str, Any]] = await league.get_league_entries_by_puuid(
        puuid=puuid
    )
    if not res:
        res = [
            {"tier": "UNRANKED", "rank": "", "leaguePoints": 0, "wins": 0, "losses": 0}
        ]

    return json(
        {
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
    app.static("/profileicon", "riot/profileicon", name="profileicon")
    app.static("/tier", "riot/tier", name="tier")
    app.static("/", "riot/dist/index.html", name="static")
    app.static("/assets", "riot/dist/assets", name="assets")
    app.static("/vite.svg", "riot/dist/vite.svg", name="favicon")
    app.before_server_start(setup_api)
    app.config.update(config)
    return app
