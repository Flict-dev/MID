from uuid import uuid4

from sqlalchemy import (
    DATE,
    UUID,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    # Именование индексов
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    # Именование уникальных индексов
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    # Именование CHECK-constraint-ов
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    # Именование внешних ключей
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    # Именование первичных ключей
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=convention)

settings_table = Table(
    "settings",
    metadata,
    Column("id", UUID, default=uuid4, index=True, primary_key=True),
    Column("city", String(length=250), index=True, nullable=True),
)

chats_table = Table(
    "chats",
    metadata,
    Column("chat_id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("is_notify", Boolean, default=False, nullable=False),
    Column("settings_id", ForeignKey("settings.id", ondelete="CASCADE"), primary_key=True),
)


structs_table = Table(
    "structs",
    metadata,
    Column("id", UUID, index=True, default=uuid4, primary_key=True),
    Column("events_path", String, nullable=False),
    Column("title_path", String, nullable=False),
    Column("date_path", String, nullable=False),
    Column("city_path", String, nullable=True),
    Column("preview_path_link", String, nullable=True),
    Column("page_link_path", String, nullable=True),
)

companies_table = Table(
    "companies",
    metadata,
    Column("id", UUID, index=True, default=uuid4, primary_key=True),
    Column("title", String(length=300), nullable=False),
    Column("url", String, nullable=False),
    Column("host", String(length=250), nullable=True),
    Column("is_active", Boolean, default=False, nullable=False),
    Column("struct_id", ForeignKey("structs.id", ondelete='CASCADE'), nullable=False),
)

events_table = Table(
    "events",
    metadata,
    Column("id", UUID, index=True, default=uuid4, primary_key=True),
    Column("title", String(length=250), nullable=False, index=True),
    Column("date", DATE, nullable=False),
    Column("city", String(length=250), nullable=True, index=True),
    Column("preview_link", String, nullable=True),
    Column("page_link", String, nullable=True),
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
)
