from logging import Logger

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from mid.src.middlewares.auth import AuthMiddleware
from mid.src.states.new_source import NewSource

logger = Logger(__file__)
router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text.lower() == "новый ресурс")
async def new_source(msg: Message, state: FSMContext):
    await msg.answer("Ввод events_url:")
    await state.set_state(NewSource.entering_events_url)


@router.message(NewSource.entering_events_url)
async def event_url_entered(msg: Message, state: FSMContext):
    await state.update_data(events_url=msg.text)
    await msg.answer("Принято, ввод events_host")
    await state.set_state(NewSource.entering_events_host)


@router.message(NewSource.entering_events_host)
async def events_container_entered(msg: Message, state: FSMContext):
    await state.update_data(events_host=msg.text)
    await msg.answer("Принято, ввод events_container")
    await state.set_state(NewSource.entering_events_container)


@router.message(NewSource.entering_events_container)
async def events_url_entered(msg: Message, state: FSMContext):
    await state.update_data(events_container=msg.text)
    await msg.answer("Принято, ввод events_title")
    await state.set_state(NewSource.entering_events_title)


@router.message(NewSource.entering_events_title)
async def events_url_entered(msg: Message, state: FSMContext):
    await state.update_data(events_title=msg.text)
    await msg.answer("Принято, ввод events_date")
    await state.set_state(NewSource.entering_events_date)


@router.message(NewSource.entering_events_date)
async def events_data_entered(msg: Message, state: FSMContext):
    await state.update_data(events_date=msg.text)
    await msg.answer("Принято, ввод events_city")
    await state.set_state(NewSource.entering_events_city)


@router.message(NewSource.entering_events_city)
async def events_city_entered(msg: Message, state: FSMContext):
    await state.update_data(events_city=msg.text)
    await msg.answer("Принято, ввод events_picture_link")
    await state.set_state(NewSource.entering_events_picture_link)


@router.message(NewSource.entering_events_picture_link)
async def events_picture_link_entered(msg: Message, state: FSMContext):
    await state.update_data(events_picture_link=msg.text)
    await msg.answer("Принято, ввод events_page_link")
    await state.set_state(NewSource.entering_events_page_link)


@router.message(NewSource.entering_events_page_link)
async def events_page_link_entered(msg: Message, state: FSMContext):
    await state.update_data(events_page_link=msg.text)
    source_data = await state.get_data()
    logger.info(source_data)
    await state.clear()
    await msg.answer("Принято!")
