import asyncio
from logging import Logger
from uuid import UUID

from aio_pika import Connection, connect_robust
from events.api.schema import Company
from events.settings import get_settings
from events.utils.deps.http_sender import HTTPSender
from events.utils.deps.local_storage import LocalStorage
from events.utils.deps.parser import Parser
from events.utils.deps.rmq_sender import RMQSender

settings = get_settings()
logger = Logger(__file__)


class EventsManager:
    async def __aenter__(self):
        self._events_storage = LocalStorage(settings.ls_path)
        # self.__rmq_connection = await connect_robust(settings.rmq_dsn)
        self._http_sender = HTTPSender()
        self._parser = Parser()
        # self._rmq_sender = RMQSender(self.__rmq_connection)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._http_sender.close()
        # await self.__rmq_connection.close()
        # await self._events_storage._write_data()

    async def _check_company(self, doc: Company):
        html = await self._http_sender.get_html(doc.url, doc.title)
        events = self._parser.parse_events(html, doc)
        # TODO: write logic for remove event from LS

        for event in events:
            print(event)
            print("===")
            # if await self._events_storage.check_event(event.title, doc.title):
            #     await self._events_storage.add_event(event.title, doc.title)
            #     await self._rmq_sender.send_event(event)

    async def check_events(self):
        ...
        # companies = await self._http_sender.get_companies(settings.db_api)
        # if companies is None:
        #     # Write allert logic here
        #     return
        # tasks = []
        # for company in companies:
        #     task = self._check_company(company)
        #     tasks.append(task)
        # await asyncio.gather(*tasks)
