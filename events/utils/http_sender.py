from logging import Logger
from random import choice
from typing import List

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from user_agent import generate_navigator

logger = Logger(__file__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProxyManager:
    def __init__(self, session: ClientSession) -> None:
        self.__session = session
        self._proxy_provider = "https://free-proxy-list.net"

    async def _get_proxies(self) -> List[str]:
        result = []
        print("=======" * 10)

        headers = generate_navigator(os=("win", "mac"))
        headers = {k: v for k, v in headers.items() if v}
        async with self.__session.get(
            self._proxy_provider, headers=headers
        ) as response:
            print("=======" * 10)
            if response.status != 200:
                logger.critical(
                    f"Free proxy website sent invalid status code {response.status}"
                )
                return result
            html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        proxy_table = soup.find("table", class_="table table-striped table-bordered")
        if not proxy_table:
            logger.critical(
                "The parser crashed with a critical error the structure of the site may have been changed!"
            )
            return result
        table_body = proxy_table.find("tbody")
        for row in table_body.find_all("tr")[5:]:
            columns = row.find_all("td")
            ip = columns[0].text
            port = columns[1].text
            protocol = "https" if columns[6].text == "yes" else "http"
            result.append(f"{protocol}://{ip}:{port}")
        return result

    async def _check_proxy(self, proxy: str) -> bool:
        async with self.__session.get(proxy) as response:
            return response.status == 200

    async def get_proxy(self) -> str | None:
        proxy_list = await self._get_proxies()
        if not proxy_list:
            logger.error("Proxy list not found!")
            return None

        proxy = choice(proxy_list)
        # while not await self._check_proxy(proxy):
        #     proxy_list.remove(proxy)
        #     if len(proxy_list) == 0:
        #         logger.error("Proxy list not found!")
        #         return None
        #     proxy = choice(proxy_list)
        return proxy


class HTTPSender(metaclass=Singleton):
    def __init__(self) -> None:
        self.__session = ClientSession()
        self._proxy_manger = ProxyManager(self.__session)

    async def get_html(self, url: str, company: str) -> str | None:
        proxy = await self._proxy_manger.get_proxy()
        headers = generate_navigator(os=("win", "mac"))
        headers = {k: v for k, v in headers.items() if v}
        async with self.__session.get(url, headers=headers) as response:
            if response.status != 200:
                logger.error(f"Request error with <{company}> at - {url}")
                return None
            return await response.text()

    async def close(self):
        await self.__session.close()
