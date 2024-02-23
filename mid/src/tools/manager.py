import asyncio
from logging import Logger
from uuid import UUID

from mid.src.settings import get_config
from mid.src.tools.deps.http_sender import HTTPSender
from mid.src.tools.deps.local_storage import LocalStorage
from mid.src.tools.deps.parser import Parser

config = get_config()
logger = Logger(__file__)


# class Manager:
