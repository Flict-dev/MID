import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from mid.src.handlers import commands
from mid.src.handlers.admin import sources
from mid.src.settings import get_config

config = get_config()
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(config.BOT_TOKEN)
    dp = Dispatcher(
        storage=RedisStorage(
            Redis(host=config.DB_HOST, port=config.DB_PORT, password=config.DB_PASSWORD)
        )
    )
    dp.include_routers(commands.router, sources.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
