from functools import lru_cache

from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # token = config("TOKEN")
    ls_path: str = "a"
    rmq_dsn: str= "a"
    # routing_key = config("ROUTING_KEY")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
