from logging import Logger
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from mid.src.settings import get_config

logger = Logger(__file__)
config = get_config()


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        if str(user.id) in config.ADMIN_IDS:
            return await handler(event, data)
        logger.warning(f"User with {user.id} id: Tried to get access to admin handlers")
