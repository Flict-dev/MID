import asyncio

from core import EventsManager
from settings import get_settings

settings = get_settings()


import asyncio
import logging

# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from sqlalchemy.ext.asyncio import create_async_engine

# from apscheduler.triggers.interval import IntervalTrigger
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
        scheduler.add_job(manager.check_events, 'interval', seconds=3)
    scheduler.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    
    asyncio.run(main())
    # asyncio.get_event_loop().run_forever()





if __name__ == "__main__":
    asyncio.run(main())
