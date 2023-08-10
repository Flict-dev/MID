from datetime import date

from pydantic import UUID4, BaseModel


class EventBase(BaseModel):
    title: str
    date: date | None
    city: str | None
    preview_link: str | None
    page_link: str
    company_id: UUID4


class ParserCardField(BaseModel):
    name: str | None
    class_: str | None


class ParserCard(BaseModel):
    host: str | None
    container: ParserCardField
    card: ParserCardField
    title: ParserCardField
    date: ParserCardField
    city: ParserCardField
    preview_link: ParserCardField
    page_link: ParserCardField


class ParserBase(BaseModel):
    struct: ParserCard
    events: list
