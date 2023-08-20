import asyncio
from typing import List

from msgspec import Struct, json

# from utils.parser import Parser
from new_parser import Parser
from schemas import ParserCard, ParserCardField
from utils.http_sender import HTTPSender


class ParserCardField(Struct):
    name: str
    class_: str


class Company(Struct):
    url: str
    container: ParserCardField
    card: ParserCardField




async def main():
    bebra = HTTPSender()
    parser = Parser()

    with open("events.json", encoding="utf-8") as f:
        data = json.decode(f.read(), type=List[ParserCard])

    # print(data)
    res = []
    # event = data[0]
    try:
        for event in data:
            html = await bebra.get_html(event.url, "yandex")
            events = parser.parce_events(html, event)
            # fi
            # for i in events:
            #     print(i)
            #     print("====" *15 )
    except Exception as e:
        print(e)
    finally:
        await bebra.close()
    # for i in res:
    #     print(i)
    #     print('=======')
    


if __name__ == "__main__":
    asyncio.run(main())
