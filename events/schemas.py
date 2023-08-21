from datetime import date
from uuid import UUID, uuid4

from msgspec import Struct, field, json


class Event(Struct):
    title: str
    date: date | None
    city: str | None
    preview_link: str | None
    page_link: str | None
    company_id: UUID
    id: UUID = field(default_factory=uuid4)

    def to_bytes(self) -> bytes:
        return json.encode({f: getattr(self, f) for f in self.__struct_fields__})

    def __str__(self) -> str:
        res = []
        for f in self.__struct_fields__:
            res.append(f"{f}: {getattr(self, f)}\n")
        return "".join(res)


class ParserCard(Struct):
    url: str | None
    host: str | None
    events: str | None
    title: str
    date: str
    city: str | None
    preview_link: str | None
    page_link: str | None


class ParserBase(Struct):
    struct: ParserCard
    events: list
