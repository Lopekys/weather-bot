import logging
import asyncio

from aiogram import Dispatcher

from core.config import bot
from core.database.init_types import init_subscription_types
from core.notification_scheduler import start_scheduler
from handlers.subscribe_handler import register_subscribe
from handlers.weather_handler import register_weather, fallback_handler

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    dp = Dispatcher()

    register_weather(dp)
    register_subscribe(dp)
    dp.message.register(fallback_handler)
    start_scheduler()

    await dp.start_polling(bot)


if __name__ == "__main__":
    init_subscription_types()
    asyncio.run(main())
