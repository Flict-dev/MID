from logging import Logger
from uuid import UUID

from aio_pika import Connection

from events.schemas import ParserCard
from events.settings import get_settings
from events.utils.http_sender import HTTPSender
from events.utils.local_storage import LocalStorage
from events.utils.parser import Parser
from events.utils.rmq_sender import RMQSender

settings = get_settings()
logger = Logger(__file__)


class EventsManager:
    def __init__(self, ls_path: str, rmq_connection: Connection) -> None:
        self.events_storage = LocalStorage(ls_path)
        self.http_sender = HTTPSender()
        self.parser = Parser()
        self.rmq_sender = RMQSender(rmq_connection)

    async def task(
        self,
        url: str,
        company: str,
        doc: ParserCard,
        company_id: UUID,
    ):
        html = await self.http_sender.get_html(url, company)
        events = self.parser.parce_events(html, doc, company_id)
        for event in events:
            if self.events_storage.check_event(event.title, company):
                await self.events_storage.add_event(event.title, company)
                await self.rmq_sender.send_event(event)
