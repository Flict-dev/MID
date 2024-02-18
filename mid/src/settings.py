from functools import lru_cache
from typing import Set

from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = config(
        "BOT_TOKEN", "6041168608:AAFaigSImDQM-lsyqoO9P_UUZo7PxROTTb8"
    )
    DB_PASSWORD: str = config("DB_PASSWORD", "localpassword")
    DB_PORT: int = config("DB_PORT", 6379)
    DB_HOST: str = config("DB_HOST", "localhost")
    ADMIN_IDS: str = config("ADMIN_IDS")


@lru_cache
def get_config() -> Settings:
    return Settings()
