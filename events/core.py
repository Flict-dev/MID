import json
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, Dict

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import UUID4
from user_agent import generate_user_agent

from events.schemes import EventBase
from events.utils.local_storage import LocalStorage
from events.utils.sender import Sender

logger = Logger(__file__)


class EventsManager:
    def __init__(self, title: str, url: str) -> None:
        self.events_storage = LocalStorage("Bebra")  # Fix this on real path
        self.sender = Sender()
        self.parcers = {} # Fix this


    async def get_event(self, url: str, company: str, company_id: UUID4):
        pass
        
        text = await self.sender.get_html(url, company)
        # event = self.__parce_html(text, company_id)
        # if not self.__events_storage.check_object(event.title):
        #         self.__events_storage.add_object(event.title)

        # self.__check_event()
        # self.__send_event_in_bot()


