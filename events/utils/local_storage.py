from logging import Logger
from typing import Dict

import aiofiles
from msgspec import json

logger = Logger(__file__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LocalStorage(metaclass=Singleton):
    """
    Yes, I know it's better to use db for storing data,
    which is used for scheduled tasks,
    but this is my project and I do whatever I want {^_^}
    """

    def __init__(self, path: str) -> None:
        raw = self.__read_data()
        self.path = path
        self.__storage = {k: set(v) for k, v in raw.items()}

    async def __read_data(self) -> Dict[str, list]:
        async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
            return json.decode(await f.read())

    async def __write_data(self, data: Dict[str, list]):
        async with aiofiles.open(self.path, "w", encoding="utf-8") as f:
            json_event = json.encode(data, indent=4)
            await f.write(json_event)

    def __check_company_name(self, company_name: str) -> bool:
        if company_name not in self.__storage.keys():
            logger.error(f"Such type as <{company_name}> doesn't exist!")
            return False
        return True

    def check_event(self, event: str, company_name: str) -> bool:
        if self.__check_company_name(company_name):
            return event in self.__storage[company_name]

    async def add_event(self, event: str, company_name: str):
        if self.__check_company_name(company_name):
            self.__storage[company_name].add(event)
        data = {k: list(v) for k, v in self.__storage.items()}
        await self.__write_data(data)

    async def remove_event(self, event: str, company_name: str):
        if self.__check_company_name(company_name):
            self.__storage[company_name].remove(event)
        data = {k: list(v) for k, v in self.__storage.items()}
        await self.__write_data(data)
