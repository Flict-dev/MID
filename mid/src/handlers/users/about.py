from aiogram import F
from aiogram.types import Message
from mid.src.static.texts import ABOUT_TEXT
from aiogram import Router


router = Router()


@router.message(F.text == "О сервисе")
async def about(message: Message):
    await message.answer(ABOUT_TEXT)
