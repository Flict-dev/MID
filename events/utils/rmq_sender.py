from aio_pika import Connection
from aio_pika.message import Message

from events.schemas import Event
from events.settings import get_settings

settings = get_settings()


class RMQSender:
    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    async def _send_message(self, message: Message, routing_key: str):
        async with self.__connection:
            channel = await self.__connection.channel()
            queue = await channel.declare_queue(routing_key, durable=True)
            await channel.default_exchange.publish(message, queue.name)

    async def send_event(self, event: Event):
        message = Message(body=event.to_bytes(), content_encoding="utf-8")
        await self._send_message(message, settings.routing_key)
