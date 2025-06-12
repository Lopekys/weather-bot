# Telegram Weather Bot

## Requirements
To run this bot locally, you need:

- **Python 3.7+**
- A **Telegram Bot Token** from [BotFather](https://core.telegram.org/bots#botfather)
- A **Weather API Key** (e.g., from [OpenWeatherMap](https://openweathermap.org/))

---

## Setup

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/Lopekys/weather-bot.git
```

### 2. Install Dependencies
Navigate to the project directory and install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project directory and add your credentials:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_openweather_api_key
```

---

## Running the Bot
To start the bot, use the following command:

```bash
python main.py
```

---

## Features

- 🌦 **Current Weather:** Get real-time weather conditions for any city around the world.
- 📅 **Forecast:** 5-day forecast with detailed 3-hour intervals; specify any number of days on demand.
- 🕒 **Hourly Forecast:** Detailed forecast for the next 24 hours in 3-hour steps.
- 🔤 **Transliteration:** Supports city name transliteration (Cyrillic) for correct API recognition.
- 🏭 **Air Quality Index:** Check air pollution and key component levels (AQI, CO, NO₂, PM2.5, and more).
- 📋 **Detailed Weather Info:** See all available weather data — min/max temperature, feels like, pressure, humidity, visibility, cloudiness, and more.
- 🌅 **Sunrise & Sunset:** Quickly view sunrise and sunset times for any city.
- 💨 **Wind Details:** Get wind speed, direction, and gusts for any city.
- 🧩 **User-Friendly Interaction:** Intuitive commands, clear formatting, and emoji for fast navigation.
- ⏱ **Real-Time Data:** Always up-to-date — directly from the OpenWeather API.


---