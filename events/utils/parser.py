from datetime import date
from logging import Logger
from time import perf_counter
from typing import List

import dateparser
from bs4 import BeautifulSoup, Tag

from events.schemes import EventBase, ParserCard, ParserCardField

logger = Logger(__file__)


class SuperParser:
    MONTHS = {
        "января",
        "феварля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентярбря",
        "октября",
        "ноября",
        "декабря",
    }

    def _parse_container(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        html_container = obj.find(data.name, class_=data.class_)
        if not html_container:
            logger.error(
                f"Error while parsing container. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
        return html_container

    def _parse_events(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        events = obj.find_all(data.name, class_=data.class_)
        if not events:
            logger.error(
                f"Error while parsing events. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
        return events

    def _parse_title(self, obj: Tag, data: ParserCardField) -> str | None:
        html_title = obj.find(data.name, class_=data.class_)
        if not html_title:
            logger.error(
                f"Error while parsing title. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None
        return html_title.text

    def _parse_city(self, obj: Tag, data: ParserCardField) -> str:
        html_city = obj.find(data.name, class_=data.class_)
        if not html_city:
            logger.error(
                f"Error while parsing city. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None
        return html_city.text

    def _parse_date(self, obj: Tag, data: ParserCardField) -> date | None:
        html_date = obj.find(data.name, class_=data.class_)
        if not html_date:
            logger.error(
                f"Error while parsing date. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None
        strings = html_date.text.split(" ")
        string_date = map(lambda x: x.isdigit() or x in self.MONTHS, strings)
        normolized_date = dateparser.parse(" ".join(string_date))

        if not normolized_date:
            logger.error(f"Error while date parsing!\nText: {string_date}")
            return None
        return normolized_date

    def _parse_preview_link(self, obj: Tag, data: ParserCardField, host: str) -> str:
        html_preview = obj.find(data.name, class_=data.class_)
        if not html_preview:
            logger.error(
                f"Error while parsing preview_link. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None

        def __parse_from_div(elemnt: Tag):
            string_style = elemnt.get("style")
            url = string_style.replace(")", "").replace("background-image:url(", "")
            if not url:
                logger.error(
                    f"Error while parsing preview_link. Field '{data.name}' with class name '{data.class_}' not found in HTML: {html_preview}"
                )
                return None
            if "http" in url:
                return url
            return host + url

        def __parse_from_img(elemnt: Tag):
            url = elemnt.get("src")
            if not url:
                logger.error(
                    f"Error while parsing preview_link. Field '{data.name}' with class name '{data.class_}' not found in HTML: {html_preview}"
                )
                return None
            return url

        if html_preview.name == "div":
            return __parse_from_div(html_preview)
        elif html_preview.name == "img":
            return __parse_from_img(html_preview)
        else:
            logger.error(
                f"Error while parsing preview_link. _parse_preview_link don't support this HTML: {html_preview}"
            )

    def _parse_page_link(self, obj: Tag, data: ParserCardField, host: str) -> str:
        html_link = obj.find(data.name, class_=data.class_)
        if not html_link:
            logger.error(
                f"Error while parsing page_link. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None
        url = html_link.get("href")
        if not url:
            logger.error(
                f"Error while parsing page_link. Href not found in HTML: {html_link}"
            )
            return None
        if "http" not in url:
            return host + url
        return url

    def parce_event(self, text: str, doc: ParserCard) -> EventBase:
        _soup = BeautifulSoup(text, "html.parser")
        container = self._parse_container(_soup, doc.container)
        events = self._parse_events(container, doc.card)

        # for event in events:
        #     s = perf_counter()
        #     title = event.find(doc.title.name, class_=doc.title.class_)

        #     city = event.find(doc.city.name, class_=doc.city.class_)
        #     preview_link = event.find(
        #         doc.preview_link.name, class_=doc.preview_link.class_
        #     )

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
