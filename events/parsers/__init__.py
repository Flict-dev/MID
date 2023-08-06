from datetime import date
from logging import Logger
from time import perf_counter
from typing import List

import dateparser
from bs4 import BeautifulSoup, Tag

from events.schemes import EventBase, ParserCard, ParserCardField

logger = Logger(__file__)


class SuperParser:
    def __init__(self) -> None:
        pass

    def _parce_container(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        container = obj.find(data.name, class_=data.class_)
        if not container:
            logger.error(f"The container was not found in the code!\nHTML: {obj}")
        return container

    def _parce_events(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        events = obj.find_all(data.name, class_=data.class_)
        if not events:
            logger.error(f"Events not found in the container!\nHTML: {obj}")
        return events

    def _parce_title(self, class_name: str) -> str:
        ...

    def _parce_city(self, class_name: str) -> str:
        ...

    def _parce_date(self, obj: Tag, data: ParserCardField) -> date:
        raw_date = obj.find(
            data.name, class_=data.class_
        )  # Think about yandex format "frontend idiots"
        normolized_date = dateparser.parse(raw_date)

    def _parce_preview_link(self, class_name: str) -> str:
        ...

    def _parce_page_link(self, class_name: str) -> str:
        ...

    def parce_event(self, text: str, doc: ParserCard) -> EventBase:
        _soup = BeautifulSoup(text, "html.parser")
        container = self._parce_container(_soup, doc.container)
        events = self._parce_container(container, doc.card)

        for event in events:
            s = perf_counter()
            title = event.find(doc.title.name, class_=doc.title.class_)

            city = event.find(doc.city.name, class_=doc.city.class_)
            preview_link = event.find(
                doc.preview_link.name, class_=doc.preview_link.class_
            )
            page_link = event.find(doc.page_link.name, class_=doc.page_link.class_)

            # print(
            #     title.text if title else None,
            #     "\n",
            #     event_date.text,
            #     city.text,
            #     preview_link,
            #     page_link["href"],
            # )
            # print(perf_counter() - s)
            # print("===" * 20)
        # title = self.


# url = "https://events.yandex.ru/"
# doc = ParserCard(
#     host="events.yandex.ru",
#     container=ParserCardField(name="div", class_="events__container"),
#     card=ParserCardField(name="div", class_="event-card"),
#     title=ParserCardField(name="a", class_="event-card__title"),
#     date=ParserCardField(name="div", class_="event-card__date"),
#     city=ParserCardField(name="div", class_="event-card__date"),
#     preview_link=ParserCardField(name="div", class_="event-card__image"),
#     page_link=ParserCardField(name="a", class_="event-card__title"),
# )


# s = perf_counter()
# response = requests.get(url)
# print(perf_counter() - s)
# s = perf_counter()
# soup = BeautifulSoup(response.content, "html.parser")
# print(perf_counter() - s)
