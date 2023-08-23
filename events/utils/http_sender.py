from logging import Logger
from typing import List

from aiohttp import ClientSession
from msgspec import json
from schemas import Company
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

    async def get_companies(self, url: str) -> List[Company]:
        async with self.__session.get(url) as response:
            if response.status != 200:
                logger.error("DB service send error!")
                return None
            json = await response.json()
            return json.decode(json, type=List[Company])

    async def close(self):
        await self.__session.close()
