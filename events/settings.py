from functools import lru_cache

from decouple import config
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LS_PATH: str = config("LS_PATH")
    RNQ_DSN: str = config("RMQ_DSN")
    PG_DSN: str = config("PG_DSN")
    ROUTING_KEY: str = config("ROUTING_KEY")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
