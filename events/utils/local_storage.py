import json
from abc import ABC, abstractmethod
from logging import Logger
from typing import Dict

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import UUID4
from user_agent import generate_user_agent

from events.schemes import EventBase

logger = Logger(__file__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LocalStorage(metaclass=Singleton):
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
