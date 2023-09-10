from datetime import datetime

from sqlalchemy import select

from events.db.schema import events_table

from .base import BaseView


class EventsView(BaseView):
    URL_PATH = "/events"

    async def get(self):
        today = datetime.date()
        query = select(events_table).where(events_table.c.date <= today)
        events = await self.pg.execute(query)
        print(events)
