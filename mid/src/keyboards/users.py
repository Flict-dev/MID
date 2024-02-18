from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def make_start_keyboard(is_admin: bool) -> ReplyKeyboardMarkup:
    btns = [
        [KeyboardButton(text="Мероприятия")],
        [KeyboardButton(text="О сервисе"), KeyboardButton(text="Фидбэк")],
    ]
    if is_admin:
        btns.append([KeyboardButton(text="Новый ресурс")])
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)
