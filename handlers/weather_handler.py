import aiohttp
import os
from aiogram.types import Message
from dotenv import load_dotenv

from utils.translit_utils import transliterate_city

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

async def get_weather(city: str) -> str:
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                text = await resp.text()
                return f"Error {resp.status}: {text}"
            data = await resp.json()
            name = data.get("name", city)
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            wind = data["wind"]["speed"]
            return (
                f"🌍 City: {name}\n"
                f"🌡️ Temperature: {temp:.1f}°C\n"
                f"☁️ Weather: {desc}\n"
                f"💨 Wind: {wind} m/s"
            )

async def message_handler(message: Message) -> None:
    if not message.text:
        await message.answer("The message is empty. Please enter a city name.")
        return

    city = message.text.strip()
    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Error during city transliteration: {e}")
        return

    resp_msg = await get_weather(city_transliterated)
    await message.answer(resp_msg)
