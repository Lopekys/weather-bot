from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

SUBSCRIBE_BTN = "Subscribe ✅"
CANCEL_BTN = "Cancel subscription ❌"
MY_SUBSCRIBE_BTN = "My subscription 📝"

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=SUBSCRIBE_BTN),
            KeyboardButton(text=CANCEL_BTN),
            KeyboardButton(text=MY_SUBSCRIBE_BTN),
        ]
    ],
    resize_keyboard=True
)

type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Weather 🌦️ (Current conditions)", callback_data="sub_type_weather")],
        [InlineKeyboardButton(text="Hourly 🕒 (Next 24 hours)", callback_data="sub_type_hourly")],
        [InlineKeyboardButton(text="Air quality 💨 (AQI index)", callback_data="sub_type_air")],
        [InlineKeyboardButton(text="Details 📋 (Humidity, pressure, etc.)", callback_data="sub_type_details")],
        [InlineKeyboardButton(text="Sun 🌅 (Sunrise & sunset)", callback_data="sub_type_sun")],
        [InlineKeyboardButton(text="Wind 💨 (Speed & direction)", callback_data="sub_type_wind")],
    ]
)
