import json
from abc import ABC
from logging import Logger
from typing import Dict

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

logger = Logger(__file__)


class LocalStorage:
    """
    Yes, I know it's better to use mongodb for storing data,
    which is used for scheduled tasks,
    but this is my project and I do whatever I want {^_^}
    """

    def __init__(self, path: str) -> None:
        raw = self.__read_data()
        self.path = path
        self.__storage = {k: set(v) for k, v in raw.items()}

    async def __read_data(self) -> Dict[str, list]:
        async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
            return json.loads(await f.read())

    async def __write_data(self, data: Dict[str, list]):
        async with aiofiles.open(self.path, "w", encoding="utf-8") as f:
            json_object = json.dumps(data, indent=4)
            await f.write(json_object)

    def __check_object_type(self, object_type: str) -> bool:
        if object_type not in self.__storage.keys():
            logger.error(f"Such type as <{object_type}> doesn't exist!")
            return False
        return True

    async def check_object(self, object: str, object_type: str = "events") -> bool:
        if self.__check_object_type(object_type):
            return object in self.__storage[object_type]

    async def add_object(self, object: str, object_type: str = "events"):
        if self.__check_object_type(object_type):
            self.__storage[object_type].add(object)
        data = {k: list(v) for k, v in self.__storage.items()}
        await self.__write_data(data)

    async def remove_object(self, object: str, object_type: str = "events"):
        if self.__check_object_type(object_type):
            self.__storage[object_type].remove(object)
        data = {k: list(v) for k, v in self.__storage.items()}
        await self.__write_data(data)


class BaseParcer(ABC):
    def __init__(self, title: str, url: str) -> None:
        self.__session = ClientSession()
        self.__soup = BeautifulSoup()
        self.__events_storage = LocalStorage("Bebra")  # Fix this on real path

    async def get_event(self, url: str, company: str):
        text = await self.__get_html(url, company)
        # self.__parce_html()
        # self.__check_event()
        # self.__send_event_in_bot()

    async def __get_html(self, url: str, company: str) -> str:
        _headers = {"user-agent": generate_user_agent()}
        async with self.__session.get(url, headers=_headers) as response:
            if response.status != 200:
                logger.error(f"Request error with <{company}> at - {url}")
            return await response.text()

    def __parce_html(self, company: str):
        raise NotImplemented("This method must be implemented!")
