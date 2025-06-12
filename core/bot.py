import logging
import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from handlers import start_handler, weather_handler

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.register(start_handler.command_start_handler, CommandStart())
    dp.message.register(weather_handler.message_handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
