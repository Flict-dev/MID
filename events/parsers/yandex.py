from bs4 import BeautifulSoup

from events.parsers import BaseParser
from events.schemes import EventBase


class YandexParcer(BaseParser):
    TITLE = "Yandex"

    def parce_html(self, text: str, company_id: str) -> EventBase:
        _soup = BeautifulSoup(text, "html.parser")
        # events = _soup.find_all("div", class_="event-card")

        # for event in events:
        #     title = event.find(
        #         "h2", class_="event-card__title"
        #     ).text.strip()  # Название мероприятия
        #     date = event.find(
        #         "div", class_="event-card__date"
        #     ).text.strip()  # Дата мероприятия

        #     # Город, если указан
        #     city_element = event.find("div", class_="event-card__city")
        #     city = city_element.text.strip() if city_element else "Город не указан"

        #     # Ссылка на картинку
        #     image_element = event.find("div", class_="event-card__image")
        #     image_url = (
        #         image_element.find("img")["src"]
        #         if image_element
        #         else "Ссылка на картинку не найдена"
        #     )
