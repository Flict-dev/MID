from logging import Logger

from aiohttp import ClientSession

logger = Logger(__file__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Sender(metaclass=Singleton):
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }

    def __init__(self) -> None:
        self.__session = ClientSession()

    async def get_html(self, url: str, company: str) -> str | None:
        async with self.__session.get(url, headers=self.HEADERS) as response:
            if response.status != 200:
                logger.error(f"Request error with <{company}> at - {url}")
                return None
        return await response.text()
