# from datetime import date
import logging
from datetime import datetime
from typing import List

import dateparser
from bs4 import BeautifulSoup, Tag
from pydantic import UUID4
from schemas import Event, ParserCard, ParserCardField

logging.basicConfig(
    filename="bebra.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__file__)


class Parser:
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

    def parce_events(
        self, text: str, doc: ParserCard, company_id: UUID4 = 1
    ) -> List[Event]:
        result = []
        _soup = BeautifulSoup(text, "html.parser")
        container = self._parse_container(_soup, doc.container)
        events = self._parse_events(container, doc.card)
        print(len(events))
        for event in events:
            title = self._parse_title(event, doc.title)
            event_date = self._parse_date(event, doc.date)
            # print(title, event_date)
            if not (event_date and title):
                continue
            event_obj = Event(
                title=title,
                date=event_date.date(),
                company_id=company_id,
                city=self._parse_city(event, doc.city),
                page_link=self._parse_page_link(event, doc.page_link, doc.host),
                preview_link=self._parse_preview_link(
                    event, doc.preview_link, doc.host
                ),
            )
            # print('*****************************')
            # print(event_obj)
            result.append(event_obj)
        # print(result)
        return result

    def _parse_container(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        html_container = obj.find(data.name, class_=data.class_)
        if not html_container:
            logger.error(
                f"Error while parsing container. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
        return html_container

    def _parse_events(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        events = obj.find_all(data.name, class_=data.class_)
        print(len(events))
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

    def _parse_city(self, obj: Tag, data: ParserCardField) -> str | None:
        html_city = obj.find(data.name, class_=data.class_)
        if not html_city:
            logger.error(
                f"Error while parsing city. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None
        return html_city.text

    def _parse_date(self, obj: Tag, data: ParserCardField) -> datetime | None:
        html_date = obj.find(data.name, class_=data.class_)
        if not html_date:
            logger.error(
                f"Error while parsing date. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
            return None
        strings = html_date.text.split(" ")

        string_date = [x for x in strings if x.isdigit() or x in self.MONTHS]
        normolized_date = dateparser.parse(" ".join(string_date))

        if not normolized_date:
            logger.error(f"Error while date parsing!\nText: {string_date}")
            return None
        return normolized_date

    def _parse_preview_link(
        self, obj: Tag, data: ParserCardField, host: str
    ) -> str | None:
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

    def _parse_page_link(
        self, obj: Tag, data: ParserCardField, host: str
    ) -> str | None:
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
