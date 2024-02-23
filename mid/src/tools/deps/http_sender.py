from logging import Logger

from aiohttp import ClientSession
from user_agent import generate_navigator

logger = Logger(__file__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HTTPSender(metaclass=Singleton):
    def __init__(self) -> None:
        self.__session = ClientSession()

    async def get_html(self, url: str, company: str) -> str | None:
        headers = generate_navigator(os=("win", "mac"))
        headers = {k: v for k, v in headers.items() if v}
        async with self.__session.get(url, headers=headers) as response:
            if response.status != 200:
                logger.error(f"Request error with <{company}> at - {url}")
                return None
            return await response.text()

    async def close(self):
        await self.__session.close()
