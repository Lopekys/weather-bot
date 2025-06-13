# ----MESSAGES FOR WEATHER HANDLER----#
START_TEXT = (
    "👋 <b>Welcome to WeatherBot!</b>\n\n"
    "I can provide you with current weather, forecast, air quality, and more for any city in the world.\n\n"
    "<b>How to use:</b>\n"
    "• /weather London - Get current weather in London\n"
    "• /forecast Paris 2 - 2 day forecast for Paris\n"
    "• /help - Full command list\n\n"
    "Just type a command to get started!"
)

HELP_TEXT = (
    "<b>Available commands:</b>\n\n"
    "/start - Welcome and quick guide\n"
    "/help - List of all commands\n"
    "/weather - Current weather in the specified city\n"
    "/forecast - Weather forecast for the city\n"
    "/hourly - Hourly forecast for the next 24 hours\n"
    "/air - Air quality index for the city\n"
    "/details - Extended weather info (humidity, pressure, etc.)\n"
    "/sun - Sunrise and sunset times\n"
    "/wind - Wind speed and direction\n"
)

CITY_REQUIRED = "Please specify a city, e.g. {example}"
TRANSLIT_ERROR = "Error during city transliteration: {error}"
API_ERROR = "Could not retrieve {what} data. Please check the spelling or try again later."
CITY_NOT_FOUND = "City not found."

# ----MESSAGES FOR SUBSCRIBE HANDLER----#
WELCOME_TEXT = "Choose an action:"
SUBSCRIBE_PROMPT = "What do you want to subscribe to?"
TYPE_PROMPT = "Select the subscription type:"
FREQ_PROMPT = "How often do you want to receive updates?"
CITY_PROMPT = "Now enter the city for updates:"
CANCEL_TEXT = "Your subscription has been cancelled."
SUCCESS_TEXT = "Subscribed to <b>{info_type}</b> updates for <b>{city}</b>{time}!"

NO_SUBSCRIPTION_TEXT = "You don't have any active subscriptions."

MY_SUBSCRIPTION_TEXT = (
    "📝 <b>Your subscription:</b>\n"
    "• <b>Type:</b> {info_type}\n"
    "• <b>City:</b> {city}\n"
    "• <b>Time(s):</b> {time}"
)

SUBSCRIBE_TIME_PROMPT = (
    "At what time do you want to receive updates? (e.g. 07:30 or 18:00)\n"
    "If you want several times a day, enter them separated by comma: 07:30, 14:00"
)
CITY_NOT_FOUND_MSG = (
    "Could not find such city. Please check your spelling and try again."
)
SUBSCRIBE_TIME_FORMAT_ERROR = "Please enter time in HH:MM format (e.g. 07:30, 18:00)"
UNKNOWN_SUBSCRIPTION_TYPE = "Unknown subscription type. Please try again."
UNKNOWN_SUBSCRIPTION_FREQUENCY = "Unknown subscription frequency. Please try again."
GENERIC_SUBSCRIPTION_ERROR = "An unexpected error occurred. Please try again later."
UNKNOWN_COMMAND = "Unknown command. Please try again."
