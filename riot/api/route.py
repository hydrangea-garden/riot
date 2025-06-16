from typing import Generic, Type, TypeVar

T = TypeVar("T")

class Route(Generic[T]):
    BASE = "https://{region}.api.riotgames.com"

    def __init__(self, method: str, path: str, response_type: Type[T], region: str = "asia"):
        self.method = method
        self.path = path
        self.region = region
        self.url = self.BASE.format(region=region) + path
        self.response_type = response_type