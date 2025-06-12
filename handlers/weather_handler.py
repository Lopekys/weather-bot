from aiogram.types import Message
import aiohttp
import os

from dotenv import load_dotenv

from utils.translit_utils import transliterate_city
from utils.weather_api import get_current_weather_full

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


# /start
async def start_handler(message: Message) -> None:
    text = (
        "👋 <b>Welcome to WeatherBot!</b>\n\n"
        "I can provide you with current weather, forecast, air quality, and more for any city in the world.\n\n"
        "<b>How to use:</b>\n"
        "• <code>/weather London</code> — Get current weather in London\n"
        "• <code>/forecast Paris</code> — 2-day forecast for Paris\n"
        "• <code>/help</code> — Full command list\n\n"
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
        "/forecast - 2-day weather forecast for the city\n"
        "/hourly - Hourly forecast for the next 24 hours\n"
        "/air - Air quality index for the city\n"
        "/details - Extended weather info (humidity, pressure, etc.)\n"
        "/sun - Sunrise and sunset times\n"
        "/wind - Wind speed and direction\n"
        "/geo - Weather by coordinates"
    )
    await message.answer(text)


# /weather <city>
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

    city_name = data.get("name", city)
    temp = data["main"].get("temp")
    desc = data["weather"][0].get("description", "").capitalize()
    wind = data["wind"].get("speed")
    humidity = data["main"].get("humidity")
    pressure = data["main"].get("pressure")
    dt = data.get("dt")
    import datetime
    time_str = (
        datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
        if dt else ""
    )

    await message.answer(
        f"🌍 City: {city_name}\n"
        f"🕒 Time: {time_str}\n"
        f"🌡️ Temperature: {temp:.1f}°C\n"
        f"☁️ Weather: {desc}\n"
        f"💨 Wind: {wind} m/s\n"
        f"💧 Humidity: {humidity}%\n"
        f"🔽 Pressure: {pressure} hPa"
    )


# /forecast <city>
async def forecast_handler(message: Message) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify a city, e.g. /forecast Paris")
        return
    city = args[1].strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return
    url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?q={city_transliterated}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                text = await resp.text()
                await message.answer(f"Error {resp.status}: {text}")
                return
            data = await resp.json()
            forecasts = data["list"]
            result = f"🌤 <b>Weather forecast for {city_transliterated}:</b>\n"
            for f in forecasts:
                dt_txt = f["dt_txt"]
                temp = f["main"]["temp"]
                desc = f["weather"][0]["description"].capitalize()
                result += f"\n<b>{dt_txt}</b> | {temp:.1f}°C, {desc}"
            await message.answer(result)


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
    url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?q={city_transliterated}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                text = await resp.text()
                await message.answer(f"Error {resp.status}: {text}")
                return
            data = await resp.json()
            forecasts = data["list"][:8]  # 8x3h = 24 hours
            result = f"🕒 <b>Hourly forecast for {city_transliterated} (next 24h):</b>\n"
            for f in forecasts:
                dt_txt = f["dt_txt"]
                temp = f["main"]["temp"]
                desc = f["weather"][0]["description"].capitalize()
                result += f"\n<b>{dt_txt}</b> | {temp:.1f}°C, {desc}"
            await message.answer(result)


async def air_handler(message: Message) -> None:
    await message.answer("Air quality index coming soon!")


# /details <city>
async def details_handler(message: Message) -> None:
    await message.answer("Detailed weather info coming soon!")


# /sun <city>
async def sun_handler(message: Message) -> None:
    await message.answer("Sunrise and sunset info coming soon!")


# /wind <city>
async def wind_handler(message: Message) -> None:
    await message.answer("Wind info coming soon!")


# /geo <lat> <lon>
async def geo_handler(message: Message) -> None:
    await message.answer("Weather by coordinates coming soon!")
