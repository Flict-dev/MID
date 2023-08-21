# import asyncio

# from aio_pika import connect_robust
# from core import EventsManager

# from events.settings import get_settings

# settings = get_settings()


# async def on_startup():
#     ...


# async def get_all_companies():
#     ...


# async def main():
#     connection = await connect_robust(settings.rmq_dsn)
#     manager = EventsManager(settings.ls_path, connection)
#     manager.task()


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import logging
from typing import List

from msgspec import Struct, json
from schemas import ParserCard
from utils.http_sender import HTTPSender
from utils.parser import Parser

logging.basicConfig(
    filename="main.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


async def main():
    bebra = HTTPSender()
    parser = Parser()

    with open("events.json", encoding="utf-8") as f:
        data = json.decode(f.read(), type=List[ParserCard])

    try:
        for event in data:
            html = await bebra.get_html(event.url, "yandex")
            events = parser.parce_events(html, event)
            for i in events:
                print(i)
                print("====" * 15)
    finally:
        await bebra.close()


if __name__ == "__main__":
    asyncio.run(main())
