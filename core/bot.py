import os
import logging
import asyncio

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from handlers import weather_handler

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.register(weather_handler.start_handler, Command("start"))
    dp.message.register(weather_handler.weather_handler, Command("weather"))
    dp.message.register(weather_handler.forecast_handler, Command("forecast"))
    dp.message.register(weather_handler.hourly_handler, Command("hourly"))
    dp.message.register(weather_handler.air_handler, Command("air"))
    dp.message.register(weather_handler.details_handler, Command("details"))
    dp.message.register(weather_handler.sun_handler, Command("sun"))
    dp.message.register(weather_handler.wind_handler, Command("wind"))
    dp.message.register(weather_handler.help_handler, Command("help"))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
