import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from mid.src.handlers import commands
from mid.src.settings import get_config

config = get_config()


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(config.BOT_TOKEN)
    print(config.DB_PASSWORD)
    dp = Dispatcher(
        storage=RedisStorage(
            Redis(host=config.DB_HOST, port=config.DB_PORT, password=config.DB_PASSWORD)
        )
    )
    dp.include_router(commands.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
