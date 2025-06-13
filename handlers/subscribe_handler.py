import re

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from core.config import WEATHER_API_KEY
from core.database.db_connector import SessionLocal
from crud.subscription import add_subscription, remove_subscription, get_user_subscriptions
from utils.format_message import get_time_text
from utils.weather_api import get_current_weather_full

from .keyboards import main_keyboard, type_keyboard, SUBSCRIBE_BTN, CANCEL_BTN, MY_SUBSCRIBE_BTN
from .messages import (
    WELCOME_TEXT, SUBSCRIBE_PROMPT, TYPE_PROMPT,
    CANCEL_TEXT, SUCCESS_TEXT, NO_SUBSCRIPTION_TEXT, MY_SUBSCRIPTION_TEXT,
    SUBSCRIBE_TIME_PROMPT, SUBSCRIBE_TIME_FORMAT_ERROR, CITY_NOT_FOUND_MSG, CITY_PROMPT
)


class SubscribeState(StatesGroup):
    info_type = State()
    time = State()
    city = State()


async def subscribe_menu_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=main_keyboard)


async def subscribe_start_handler(message: Message, state: FSMContext):
    await message.answer(SUBSCRIBE_PROMPT, reply_markup=main_keyboard)
    await message.answer(TYPE_PROMPT, reply_markup=type_keyboard)
    await state.set_state(SubscribeState.info_type)


async def subscribe_cancel_handler(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    with SessionLocal() as db:
        remove_subscription(db, telegram_id)
    await state.clear()
    await message.answer(CANCEL_TEXT, reply_markup=main_keyboard)


async def subscribe_type_callback_handler(callback: CallbackQuery, state: FSMContext):
    info_type = callback.data.replace("sub_type_", "")
    await state.update_data(info_type=info_type)
    await callback.message.answer(SUBSCRIBE_TIME_PROMPT)
    await state.set_state(SubscribeState.time)
    await callback.answer()


async def subscribe_time_handler(message: Message, state: FSMContext):
    user_times = message.text.strip()
    time_list = [
        t.strip() for t in user_times.split(",")
        if re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t.strip())
    ]
    if not time_list:
        await message.answer(SUBSCRIBE_TIME_FORMAT_ERROR)
        return
    await state.update_data(time_list=time_list)
    await message.answer(CITY_PROMPT)
    await state.set_state(SubscribeState.city)


async def subscribe_city_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    info_type = data.get("info_type")
    time_list = data.get("time_list", [])
    city = message.text.strip()
    telegram_id = message.from_user.id

    weather_data = await get_current_weather_full(city, WEATHER_API_KEY)
    if not weather_data:
        await message.answer(CITY_NOT_FOUND_MSG, reply_markup=main_keyboard)
        return

    with SessionLocal() as db:
        for user_time in time_list:
            add_subscription(db, telegram_id, city, info_type, user_time)

    await message.answer(
        SUCCESS_TEXT.format(
            info_type=info_type,
            city=city,
            time=f", Time(s): {', '.join(time_list)}" if time_list else ""
        ),
        reply_markup=main_keyboard
    )
    await state.clear()


async def handle_my_subscription(message: Message):
    telegram_id = message.from_user.id
    with SessionLocal() as db:
        subs = get_user_subscriptions(db, telegram_id)
        if not subs:
            await message.answer(NO_SUBSCRIPTION_TEXT, reply_markup=main_keyboard)
            return

        lines = []
        for sub in subs:
            info_type = sub.subscription_type.description if hasattr(sub, "subscription_type") else sub.info_type
            lines.append(
                MY_SUBSCRIPTION_TEXT.format(
                    info_type=info_type,
                    city=sub.city,
                    time=get_time_text(sub.time),
                )
            )
        await message.answer("\n\n".join(lines), reply_markup=main_keyboard)


def register_subscribe(dp):
    dp.message.register(subscribe_menu_handler, Command("subscribe"))
    dp.message.register(subscribe_start_handler, lambda m: m.text == SUBSCRIBE_BTN)
    dp.message.register(subscribe_cancel_handler, lambda m: m.text == CANCEL_BTN)
    dp.message.register(handle_my_subscription, lambda m: m.text == MY_SUBSCRIBE_BTN)
    dp.callback_query.register(subscribe_type_callback_handler, lambda c: c.data.startswith("sub_type_"),
                               StateFilter(SubscribeState.info_type))
    dp.message.register(subscribe_time_handler, StateFilter(SubscribeState.time))
    dp.message.register(subscribe_city_handler, StateFilter(SubscribeState.city))
