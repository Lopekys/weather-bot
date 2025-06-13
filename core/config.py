import os

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.enums import ParseMode

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
