from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types

from core.config import WEATHER_API_KEY
from handlers.subscribe_handler import main_keyboard
from handlers.messages import (
    START_TEXT, HELP_TEXT, CITY_REQUIRED,
    TRANSLIT_ERROR, API_ERROR, CITY_NOT_FOUND, UNKNOWN_COMMAND,
)
from utils.format_message import (
    group_forecasts_by_day, format_forecast_message, format_hourly_message,
    format_weather_message, format_air_quality_message, format_details_message,
    format_sunrise_sunset_message, format_wind_message,
)
from utils.translit_utils import transliterate_city
from utils.weather_api import (
    get_current_weather_full, get_forecast_json,
    get_city_coordinates, get_air_quality,
)


def parse_city_and_handle_errors(example_command):
    def decorator(func):
        async def wrapper(message: Message, *args, **kwargs):
            command = message.text.split(maxsplit=1)
            if len(command) < 2:
                await message.answer(CITY_REQUIRED.format(example=example_command))
                return
            city = command[1].strip()
            try:
                city_transliterated = transliterate_city(city)
            except Exception as e:
                await message.answer(TRANSLIT_ERROR.format(error=e))
                return
            return await func(message, city_transliterated, *args, **kwargs)

        return wrapper

    return decorator


async def start_handler(message: Message) -> None:
    await message.answer(START_TEXT, reply_markup=main_keyboard)


async def help_handler(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=main_keyboard)


@parse_city_and_handle_errors("/weather London")
async def weather_handler(message: Message, city, **kwargs):
    data = await get_current_weather_full(city, WEATHER_API_KEY)
    if not data:
        await message.answer(API_ERROR.format(what="weather"))
        return
    msg = format_weather_message(data)
    await message.answer(msg)


@parse_city_and_handle_errors("/details Rome")
async def details_handler(message: Message, city, **kwargs):
    data = await get_current_weather_full(city, WEATHER_API_KEY)
    if not data:
        await message.answer(API_ERROR.format(what="detailed weather"))
        return
    msg = format_details_message(data)
    await message.answer(msg)


@parse_city_and_handle_errors("/sun Rome")
async def sun_handler(message: Message, city, **kwargs):
    data = await get_current_weather_full(city, WEATHER_API_KEY)
    if not data:
        await message.answer(API_ERROR.format(what="sun info"))
        return
    msg = format_sunrise_sunset_message(data)
    await message.answer(msg)


@parse_city_and_handle_errors("/wind Rome")
async def wind_handler(message: Message, city, **kwargs):
    data = await get_current_weather_full(city, WEATHER_API_KEY)
    if not data:
        await message.answer(API_ERROR.format(what="wind info"))
        return
    msg = format_wind_message(data)
    await message.answer(msg)


@parse_city_and_handle_errors("/hourly Rome")
async def hourly_handler(message: Message, city, **kwargs):
    data = await get_forecast_json(city, WEATHER_API_KEY)
    if not data:
        await message.answer(API_ERROR.format(what="forecast"))
        return
    forecasts = data.get("list", [])
    result = format_hourly_message(city, forecasts)
    await message.answer(result)


@parse_city_and_handle_errors("/air Paris")
async def air_handler(message: Message, city, **kwargs):
    lat, lon = await get_city_coordinates(city, WEATHER_API_KEY)
    if not lat or not lon:
        await message.answer(CITY_NOT_FOUND)
        return
    data = await get_air_quality(lat, lon, WEATHER_API_KEY)
    if not data or "list" not in data or not data["list"]:
        await message.answer(API_ERROR.format(what="air quality"))
        return
    msg = format_air_quality_message(city, data["list"][0])
    await message.answer(msg)


@parse_city_and_handle_errors("/forecast Paris 2")
async def forecast_handler(message: Message, city, **kwargs):
    args = message.text.split()
    days = 2
    if len(args) >= 3:
        try:
            days = int(args[2])
            if days < 1 or days > 5:
                days = 2
        except ValueError:
            pass

    city_name = args[1]
    data = await get_forecast_json(city_name, WEATHER_API_KEY)
    if not data:
        await message.answer(API_ERROR.format(what="forecast"))
        return

    forecasts = data.get("list", [])
    max_intervals = min(days * 8, len(forecasts))
    grouped = group_forecasts_by_day(forecasts, max_intervals)
    result = format_forecast_message(city_name, grouped, days)
    await message.answer(result)


async def fallback_handler(message: types.Message):
    if message.text.startswith('/'):
        await message.reply(UNKNOWN_COMMAND)


def register_weather(dp):
    dp.message.register(start_handler, Command("start"))
    dp.message.register(help_handler, Command("help"))
    dp.message.register(weather_handler, Command("weather"))
    dp.message.register(forecast_handler, Command("forecast"))
    dp.message.register(hourly_handler, Command("hourly"))
    dp.message.register(air_handler, Command("air"))
    dp.message.register(details_handler, Command("details"))
    dp.message.register(sun_handler, Command("sun"))
    dp.message.register(wind_handler, Command("wind"))
