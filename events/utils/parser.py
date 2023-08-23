import logging
from datetime import datetime
from io import StringIO
from time import time
from typing import List

import dateparser
from lxml import etree
from lxml.etree import _Element
from pydantic import UUID4
from schemas import Company, Event

logger = logging.getLogger(__file__)


class Parser:
    def __init__(self) -> None:
        self.__html_parser = etree.HTMLParser()

    def parse_events(self, text: str, doc: Company) -> List[Event]:
        result = []
        tree = etree.parse(StringIO(text), self.__html_parser)
        events = self._parse_events(tree, doc.parse_struct.events)
        if events is None:
            return result
        for i in range(1, len(events)):
            title = self._parse_title(tree, doc.title.format(index=i))
            event_date = self._parse_date(tree, doc.parse_struct.date.format(index=i))
            if not (event_date and title) or event_date.timestamp() < time():
                continue
            result.append(
                Event(
                    title=title.strip(),
                    date=event_date,
                    company_id=doc.id,
                    city=self._parse_city(tree, doc.parse_struct.city.format(index=i)),
                    page_link=self._parse_page_link(
                        tree, doc.parse_struct.page_link.format(index=i), doc.host
                    ),
                    preview_link=self._parse_preview_link(
                        tree, doc.parse_struct.preview_link.format(index=i), doc.host
                    ),
                )
            )
        return result

    def __find_by_xpath(
        self, tree, path: str, element: str, is_single: bool = True
    ) -> List[_Element] | _Element | None:
        if not path:
            logger.error(f"Error while parsing {element}.\n XPATH: {path}")
            return None
        objects: List[_Element] = tree.xpath(path)
        if not objects:
            logger.error(f"Error while parsing {element}.\n XPATH: {path}")
            return None
        return objects[0] if is_single else objects

    def _parse_events(self, tree, events_path: str) -> List[_Element] | None:
        events = self.__find_by_xpath(tree, events_path, "events", False)
        return events

    def _parse_title(self, tree, title_path: str) -> str | None:
        title = self.__find_by_xpath(tree, title_path, "title")
        return title.text if title is not None else None

    def _parse_city(self, tree, city_path: str) -> str | None:
        city = self.__find_by_xpath(tree, city_path, "city")
        return city.text if city is not None else None

    def _parse_date(self, tree, date_path: str) -> datetime | None:
        date = self.__find_by_xpath(tree, date_path, "date")
        if date is not None and date.text is not None:
            return dateparser.parse(date.text)
        return None

    def _parse_preview_link(self, tree, preview_path: str, host: str) -> str | None:
        preview = self.__find_by_xpath(tree, preview_path, "preview")

        def _parse_from_div(elemnt: _Element):
            string_style = elemnt.get("style")
            url = (
                string_style.replace(")", "")
                .replace("background-image:", "")
                .replace("url(", "")
                .strip()
            )
            if not url:
                logger.error(f"Error _parse_from_div url dont found!")
                return None
            return host + url if "http" not in url else url

        def _parse_from_img(elemnt: _Element):
            url = elemnt.get("src")
            if not url:
                logger.error(f"Error _parse_from_img url dont found!")
                return None
            return host + url if "http" not in url else url

        if preview is not None:
            if preview.tag == "div":
                return _parse_from_div(preview)
            elif preview.tag == "img":
                return _parse_from_img(preview)
            else:
                logger.error(
                    f"Error _parse_preview_link don't support this HTML: {preview.tag}"
                )
        return None

    def _parse_page_link(self, tree, link_path: str, host: str) -> str | None:
        link = self.__find_by_xpath(tree, link_path, "link")
        if link is not None:
            url = link.get("href")
            return host + url if "http" not in url else url
        return None
