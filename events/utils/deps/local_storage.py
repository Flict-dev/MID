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
        self.path = path
        self.__storage = {}

    async def _read_data(self) -> Dict[str, list]:
        async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
            return json.decode(await f.read())

    async def _write_data(self):
        async with aiofiles.open(self.path, "w", encoding="utf-8") as f:
            data = {k: list(v) for k, v in self.__storage.items()}
            json_event = json.encode(data, indent=4)
            await f.write(json_event)

    async def __check_company_name(self, company_name: str):
        if company_name not in self.__storage.keys():
            self.__storage[company_name] = set()
            logger.warn(f"Such company as <{company_name}> doesn't exist!")
            await self._write_data()

    async def check_event(self, event: str, company_name: str) -> bool:
        if not self.__storage:
            raw = await self._read_data()
            self.__storage = {k: set(v) for k, v in raw.items()}
        await self.__check_company_name(company_name)
        return event in self.__storage[company_name]

    async def add_event(self, event: str, company_name: str):
        await self.__check_company_name(company_name)
        self.__storage[company_name].add(event)
        await self._write_data()

    async def remove_event(self, event: str, company_name: str):
        await self.__check_company_name(company_name)
        self.__storage[company_name].remove(event)
        await self._write_data()
