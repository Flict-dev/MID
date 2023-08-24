import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from events.settings import get_settings
from events.utils.manager import EventsManager

settings = get_settings()


logging.basicConfig(
    filename="main.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


async def main():
    scheduler = AsyncIOScheduler()
    async with EventsManager() as manager:
        scheduler.add_job(
            manager.check_events, "interval", seconds=3, id="check_events"
        )
    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
