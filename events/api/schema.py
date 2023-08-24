from datetime import date
from uuid import UUID

from msgspec import Struct, json


class Event(Struct):
    title: str
    date: date | None
    city: str | None
    preview_link: str | None
    page_link: str | None
    company_id: UUID

    def to_bytes(self) -> bytes:
        return json.encode({f: getattr(self, f) for f in self.__struct_fields__})

    def __str__(self) -> str:
        res = []
        for f in self.__struct_fields__:
            res.append(f"{f}: {getattr(self, f)}\n")
        return "".join(res)


class CompanyCard(Struct):
    title: str
    date: str
    url: str | None
    host: str | None
    events: str | None
    city: str | None
    preview_link: str | None
    page_link: str | None


class Company(Struct):
    id: UUID
    title: str
    url: str
    host: str
    parse_struct: CompanyCard
    is_active: bool
