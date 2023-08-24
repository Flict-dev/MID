# Draft
# class ProxyManager:
#     def __init__(self, session: ClientSession) -> None:
#         self.__session = session
#         self._proxy_provider = "https://free-proxy-list.net"

#     async def _get_proxies(self) -> List[str]:
#         result = []
#         print("=======" * 10)

#         headers = generate_navigator(os=("win", "mac"))
#         headers = {k: v for k, v in headers.items() if v}
#         async with self.__session.get(
#             self._proxy_provider, headers=headers
#         ) as response:
#             print("=======" * 10)
#             if response.status != 200:
#                 logger.critical(
#                     f"Free proxy website sent invalid status code {response.status}"
#                 )
#                 return result
#             html = await response.text()
#         soup = BeautifulSoup(html, "html.parser")
#         proxy_table = soup.find("table", class_="table table-striped table-bordered")
#         if not proxy_table:
#             logger.critical(
#                 "The parser crashed with a critical error the structure of the site may have been changed!"
#             )
#             return result
#         table_body = proxy_table.find("tbody")
#         for row in table_body.find_all("tr")[5:]:
#             columns = row.find_all("td")
#             ip = columns[0].text
#             port = columns[1].text
#             protocol = "https" if columns[6].text == "yes" else "http"
#             result.append(f"{protocol}://{ip}:{port}")
#         return result

#     async def _check_proxy(self, proxy: str) -> bool:
#         async with self.__session.get(proxy) as response:
#             return response.status == 200

#     async def get_proxy(self) -> str | None:
#         proxy_list = await self._get_proxies()
#         if not proxy_list:
#             logger.error("Proxy list not found!")
#             return None

#         proxy = choice(proxy_list)
#         # while not await self._check_proxy(proxy):
#         #     proxy_list.remove(proxy)
#         #     if len(proxy_list) == 0:
#         #         logger.error("Proxy list not found!")
#         #         return None
#         #     proxy = choice(proxy_list)
#         return proxy