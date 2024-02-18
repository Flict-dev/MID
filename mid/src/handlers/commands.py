from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from mid.src.keyboards.users import make_start_keyboard
from mid.src.settings import get_config
from mid.src.static.texts import START_TEXT

router = Router()
config = get_config()


@router.message(Command("start"))
async def start(msg: Message):
    is_admin = str(msg.from_user.id) in config.ADMIN_IDS
    keyboard = make_start_keyboard(is_admin)
    await msg.answer(START_TEXT, reply_markup=keyboard)
