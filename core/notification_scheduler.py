import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from core.config import bot, WEATHER_API_KEY
from core.database.db_connector import SessionLocal
from crud.subscription import get_subscriptions_by_time
from utils.weather_api import (
    get_current_weather_full, get_city_coordinates, get_air_quality, get_forecast_json
)
from utils.format_message import (
    format_weather_message, format_hourly_message, format_details_message,
    format_sunrise_sunset_message, format_wind_message, format_air_quality_message
)

scheduler = AsyncIOScheduler()


async def send_notification(telegram_id, message):
    if message:
        await bot.send_message(telegram_id, message)


async def check_and_send_notifications():
    current_time = datetime.datetime.now().strftime('%H:%M')
    with SessionLocal() as db:
        subscriptions = get_subscriptions_by_time(db, current_time)
        tasks = []
        for subscription in subscriptions:
            sub_type = getattr(getattr(subscription, "subscription_type", None), "code", None)
            if not sub_type:
                continue

            msg = None
            city = subscription.city

            if sub_type == "weather":
                weather = await get_current_weather_full(city, WEATHER_API_KEY)
                if weather:
                    msg = format_weather_message(weather)

            elif sub_type == "hourly":
                forecast = await get_forecast_json(city, WEATHER_API_KEY)
                if forecast and "list" in forecast:
                    msg = format_hourly_message(city, forecast["list"])

            elif sub_type == "details":
                weather = await get_current_weather_full(city, WEATHER_API_KEY)
                if weather:
                    msg = format_details_message(weather)

            elif sub_type == "sun":
                weather = await get_current_weather_full(city, WEATHER_API_KEY)
                if weather:
                    msg = format_sunrise_sunset_message(weather)

            elif sub_type == "wind":
                weather = await get_current_weather_full(city, WEATHER_API_KEY)
                if weather:
                    msg = format_wind_message(weather)

            elif sub_type == "air":
                lat, lon = await get_city_coordinates(city, WEATHER_API_KEY)
                air = await get_air_quality(lat, lon, WEATHER_API_KEY)
                if air and "list" in air and air["list"]:
                    msg = format_air_quality_message(city, air["list"][0])

            if msg:
                tasks.append(send_notification(subscription.user.telegram_id, msg))

        if tasks:
            await asyncio.gather(*tasks)


def start_scheduler():
    scheduler.add_job(check_and_send_notifications, 'cron', minute='*')
    scheduler.start()
