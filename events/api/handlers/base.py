from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_urldispatcher import View
from asyncpgsa import PG


class BaseView(View):
    URL_PATH: str

    @property
    def pg(self) -> PG:
        return self.request.app['pg']
    
    