def main() -> None:  # pragma: no cover
    # I've done all of my testing on this.
    from functools import partial
    from sys import argv

    from sanic import Sanic
    from sanic.worker.loader import AppLoader

    from riot.argparser import parse_args
    from riot.config import ServerConfig
    from riot.server import create_app

    server_config = ServerConfig()

    args = parse_args(argv[1:])
    server_config.update_with_args(args)

    loader = AppLoader(factory=partial(create_app, server_config))
    app = (  # pyright: ignore[reportUnknownVariableType]
        loader.load()  # pyright: ignore[reportUnknownMemberType]
    )

    app.prepare(  # pyright: ignore[reportUnknownMemberType]
        server_config.HOST,
        server_config.PORT,
        debug=server_config.DEBUG,
        workers=server_config.WORKERS,
    )

    Sanic.serve(app, app_loader=loader)  # pyright: ignore[reportUnknownMemberType]


if __name__ == "__main__":  # pragma: no cover
    main()
