import os

from aiogram.types import Message
from dotenv import load_dotenv

from utils.format_message import (
    group_forecasts_by_day,
    format_forecast_message,
    format_hourly_message,
    format_weather_message,
    format_air_quality_message,
    format_details_message,
    format_sunrise_sunset_message,
    format_wind_message,
)
from utils.translit_utils import transliterate_city
from utils.weather_api import (
    get_current_weather_full,
    get_forecast_json,
    get_city_coordinates,
    get_air_quality,
)

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


# /start
async def start_handler(message: Message) -> None:
    text = (
        "👋 <b>Welcome to WeatherBot!</b>\n\n"
        "I can provide you with current weather, forecast, air quality, and more for any city in the world.\n\n"
        "<b>How to use:</b>\n"
        "•/weather London - Get current weather in London\n"
        "•/forecast Paris 2 - 2 day forecast for Paris\n"
        "•/help - Full command list\n\n"
        "Just type a command to get started!"
    )
    await message.answer(text)


# /help
async def help_handler(message: Message) -> None:
    text = (
        "<b>Available commands:</b>\n\n"
        "/start - Welcome and quick guide\n"
        "/help - List of all commands\n"
        "/weather - Current weather in the specified city\n"
        "/forecast - weather forecast for the city\n"
        "/hourly - Hourly forecast for the next 24 hours\n"
        "/air - Air quality index for the city\n"
        "/details - Extended weather info (humidity, pressure, etc.)\n"
        "/sun - Sunrise and sunset times\n"
        "/wind - Wind speed and direction\n"
    )
    await message.answer(text)


# /current weather
async def weather_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /weather London")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    data = await get_current_weather_full(city_transliterated, WEATHER_API_KEY)
    if not data:
        await message.answer("Error: could not retrieve weather data.")
        return

    msg = format_weather_message(data)
    await message.answer(msg)


# /forecast for n day
async def forecast_handler(message: Message) -> None:
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /forecast Paris 2")
        return
    city = args[1].strip()
    days = 2
    if len(args) == 3:
        try:
            days = int(args[2])
            if days < 1 or days > 5:
                days = 2
        except ValueError:
            pass

    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    data = await get_forecast_json(city_transliterated, WEATHER_API_KEY)
    if not data:
        await message.answer("Error: could not retrieve forecast.")
        return

    forecasts = data.get("list", [])
    max_intervals = min(days * 8, len(forecasts))
    grouped = group_forecasts_by_day(forecasts, max_intervals)
    result = format_forecast_message(city_transliterated, grouped, days)
    await message.answer(result)


# /forecast for 24 h
async def hourly_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /hourly Rome")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    data = await get_forecast_json(city_transliterated, WEATHER_API_KEY)
    if not data:
        await message.answer("Error: could not retrieve forecast.")
        return

    forecasts = data.get("list", [])
    result = format_hourly_message(city_transliterated, forecasts)
    await message.answer(result)


# /air  quality
async def air_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /air Paris")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    lat, lon = await get_city_coordinates(city_transliterated, WEATHER_API_KEY)
    if not lat or not lon:
        await message.answer("City not found.")
        return

    data = await get_air_quality(lat, lon, WEATHER_API_KEY)
    if not data or "list" not in data or not data["list"]:
        await message.answer("Error: could not retrieve air quality data.")
        return

    msg = format_air_quality_message(city_transliterated, data["list"][0])
    await message.answer(msg)


# /Detailed weather
async def details_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /details Rome")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    data = await get_current_weather_full(city_transliterated, WEATHER_API_KEY)
    if not data:
        await message.answer("Error: could not retrieve detailed weather data.")
        return

    msg = format_details_message(data)
    await message.answer(msg)


# /sunrise and sunset
async def sun_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /sun Rome")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    data = await get_current_weather_full(city_transliterated, WEATHER_API_KEY)
    if not data:
        await message.answer("Error: could not retrieve sun info.")
        return

    msg = format_sunrise_sunset_message(data)
    await message.answer(msg)


# /wind
async def wind_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /wind Rome")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    data = await get_current_weather_full(city_transliterated, WEATHER_API_KEY)
    if not data:
        await message.answer("Error: could not retrieve wind info.")
        return

    msg = format_wind_message(data)
    await message.answer(msg)
