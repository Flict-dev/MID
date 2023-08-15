import asyncio

from aio_pika import connect_robust
from core import EventsManager

from events.settings import get_settings

settings = get_settings()


async def on_startup():
    ...
async def get_all_companies():
    ...

async def main():
    connection = await connect_robust(settings.rmq_dsn)
    manager = EventsManager(settings.ls_path, connection)
    manager.task()

if __name__ == "__main__":
    asyncio.run(main())
