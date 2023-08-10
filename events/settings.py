from decouple import config
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token = config("TOKEN")
    pg_dsn = PostgresDsn("postgres://user:pass@localhost:5432/foobar")

