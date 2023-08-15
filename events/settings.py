from functools import lru_cache

from decouple import config
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token = config("TOKEN")
    pg_dsn = PostgresDsn("postgres://user:pass@localhost:5432/foobar")
    ls_path = ""
    rmq_dsn = ""
    routing_key = config("ROUTING_KEY")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
