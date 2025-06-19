from argparse import Namespace
from json import loads
from typing import Any, Callable, Optional, Sequence, Union, cast

from sanic.config import SANIC_PREFIX, Config


def list_converter(value: str) -> list[Any]:
    if value.startswith("["):
        return cast(list[Any], loads(value))
    raise ValueError


class ServerConfig(Config):
    def __init__(
        self,
        defaults: dict[str, Union[str, bool, int, float, None]] = {},
        env_prefix: Optional[str] = SANIC_PREFIX,
        keep_alive: Optional[bool] = None,
        *,
        converters: Optional[Sequence[Callable[[str], Any]]] = [list_converter],
    ):
        # Default
        self.update(
            {
                "CONFIG": "",
                "PRODUCTION": False,
                "USE_ENV": False,
                "DB_URL": "",
                "RIOT_API_KEY": "",
                # Sanic config
                "HOST": "127.0.0.1",
                "PORT": 8000,
                "WORKERS": 1,
                "DEBUG": False,
                "ACCESS_LOG": False,
                "FORWARDED_SECRET": "",
                # Sanic ext config
                "OAS_UI_DEFAULT": "swagger",
                "OAS_URI_REDOC": False,
                # Open API config
                "SWAGGER_UI_CONFIGURATION": {
                    "apisSorter": "alpha",
                    "operationsSorter": "alpha",
                },
                "API_TITLE": "Server",
                "API_DESCRIPTION": "Riot API wrapper ",
            }
        )
        super().__init__(
            defaults={**{"_FALLBACK_ERROR_FORMAT": "json"}, **defaults},
            env_prefix=env_prefix,
            keep_alive=keep_alive,
            converters=converters,
        )

    USE_ENV: bool
    CONFIG: str
    PRODUCTION: bool
    DB_URL: str
    RIOT_API_KEY: str
    # Sanic config
    DEBUG: bool
    HOST: str
    PORT: int
    WORKERS: int

    def load_config_with_config_json(self, path: str) -> None:
        with open(path, "r") as f:
            config = loads(f.read())
            self.update_config(config)  # pyright: ignore[reportUnknownMemberType]
        return None

    def update_with_args(self, args: Namespace) -> None:
        if not self.USE_ENV:
            self.update_config(  # pyright: ignore[reportUnknownMemberType]
                {k.upper(): v for k, v in vars(args).items()}
            )
        if self.CONFIG:
            self.load_config_with_config_json(self.CONFIG)
        return None
