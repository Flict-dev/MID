from datetime import date
from uuid import UUID, uuid4

from msgspec import Struct, field, json


class Event(Struct):
    id: UUID = field(default_factory=uuid4)
    title: str
    date: date | None
    city: str | None
    preview_link: str | None
    page_link: str
    company_id: UUID

    def to_bytes(self) -> bytes:
        return json.encode({f: getattr(self, f) for f in self.__struct_fields__})


class ParserCardField(Struct):
    name: str | None
    class_: str | None


class ParserCard(Struct):
    host: str | None
    container: ParserCardField
    card: ParserCardField
    title: ParserCardField
    date: ParserCardField
    city: ParserCardField
    preview_link: ParserCardField
    page_link: ParserCardField


class ParserBase(Struct):
    struct: ParserCard
    events: list
