import python_weather
from python_weather import Client as WeatherClient

from aiogram.types import Message
from utils.translit_utils import transliterate_city


async def message_handler(message: Message) -> None:
    if not message.text:
        await message.answer("Сообщение пустое. Пожалуйста, введите название города.")
        return

    city = message.text.strip()

    try:
        city_transliterated = transliterate_city(city)
    except Exception as e:
        await message.answer(f"Ошибка при транслитерации города: {e}")
        return

    async with WeatherClient(unit=python_weather.METRIC) as client:
        try:
            weather = await client.get(city_transliterated)

            celsius = weather.temperature
            sky_description = weather.description

            resp_msg = (
                f"🌍 Город: {city_transliterated}\n"
                f"🌡️ Температура: {celsius:.1f}°C\n"
                f"☁️ Погода: {sky_description}"
            )
            await message.answer(resp_msg)
        except Exception as e:
            await message.answer(f"❌ Не удалось получить данные о погоде для '{city}'. Ошибка: {e}")
