from aiogram.fsm.state import State, StatesGroup


class NewSource(StatesGroup):
    entering_events_url = State()
    entering_events_host = State()
    entering_events_container = State()
    entering_events_title = State()
    entering_events_date = State()
    entering_events_city = State()
    entering_events_picture_link = State()
    entering_events_page_link = State()
