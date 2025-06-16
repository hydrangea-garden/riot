from argparse import ArgumentParser, Namespace


def parse_args(argv: list[str]) -> Namespace:
    parser = ArgumentParser("server")

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The hostname to listen on (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The port of the webserver (default: 8000)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="The number of worker processes to spawn (default: 1)",
    )

    parser.add_argument(
        "--access-log",
        action="store_false",
        default=True,
        help="Disable the access log (default: False)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="The debug mode to use (default: False)",
    )

    config = parser.add_argument_group("config")

    config.add_argument(
        "--production",
        action="store_true",
        default=False,
        help="Run the server in production mode (default: False)",
    )

    config.add_argument(
        "--db-url",
        type=str,
        default="",
        help="The database URL to use (default: '')",
    )

    config.add_argument(
        "--riot-api-key",
        type=str,
        default="",
        help="The Riot API key to use (default: '')",
    )

    config.add_argument(
        "--config",
        type=str,
        default="",
        help="The path to the config file (default: '')",
    )

    return parser.parse_args(argv)
