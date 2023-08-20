# from datetime import date
from datetime import datetime
from io import StringIO
from logging import Logger
from typing import List

import dateparser
from bs4 import BeautifulSoup, Tag
from lxml import etree
from pydantic import UUID4
from schemas import Event, ParserCard, ParserCardField

logger = Logger(__file__)


class Parser:
    def parce_events(self, text: str, doc: ParserCard) -> List[Event]:
        # result = []
        html_parser = etree.HTMLParser()
        tree = etree.parse(StringIO(text), html_parser)
        bebra: List[etree._Element ]= tree.xpath('//*[@id="__next"]/div/div[2]/div[3]/div/a')
        title_path = '//*[@id="__next"]/div/div[2]/div[3]/div/a[{index}]/div[2]/div[2]'
        date_path = '//*[@id="__next"]/div/div[2]/div[3]/div/a[{index}]/div[2]/div[1]'
        city_path ='//*[@id="__next"]/div/div[2]/div[3]/div/a[{index}]/div[2]/div[3]/div[2]/div/div'
        preview_path = '//*[@id="__next"]/div/div[2]/div[3]/div/a[{index}]/div[1]'
        for i in range(1, len(bebra)):
            title = bebra[i].xpath(title_path.format(index=i))            
            date = bebra[i].xpath(date_path.format(index=i))            
            city = bebra[i].xpath(city_path.format(index=i))
            preview = bebra[i].xpath(preview_path.format(index=i))
            print(title[0].text)
            print(dateparser.parse(date[0].text))
            print(city[0].text if city else 'City None!')
            print(preview[0].get('style'))
            print('@@@@'* 10)
            

            # for child in bebra:
            #     print(child.get('href'))
        # _soup = BeautifulSoup(text, "html.parser")
        # container = self._parse_container(_soup, doc.container)
        # events = self._parse_events(container, doc.card)
        # for event in events:
        #     bebra = []
        #     for obj in event.descendants:
        #         # print(obj)
        #         if "<a" in obj.__str__():
        #             print(obj)
        #         # print(re.search(lox, ))
        #         print('=====' * 10)
        #         # if obj.text not in bebra:

        #             # bebra.append(obj.text)
        #         # result.append(obj.)
        #     result.append(' '.join(bebra))
        # print(result)
        # for i in result:
        # print(i)
        # print('==========')
        # print(len(event.descendants))
        # print(event.descendants)

    def _parse_events(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        events = obj.find_all(data.name, class_=data.class_)
        if not events:
            logger.error(
                f"Error while parsing events. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
        return events

    def _parse_container(self, obj: Tag, data: ParserCardField) -> List[Tag]:
        html_container = obj.find(data.name, class_=data.class_)
        if not html_container:
            logger.error(
                f"Error while parsing container. Field '{data.name}' with class name '{data.class_}' not found in HTML: {obj}"
            )
        return html_container
