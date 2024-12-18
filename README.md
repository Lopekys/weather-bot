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
- 🌦 **Weather Updates**: Get current weather information for any city around the world.
- 🔤 **Transliteration**: Supports transliteration of non-Latin city names into a format that the weather API can recognize.
- 🧩 **User-friendly Interaction**: Easy-to-use commands and inline buttons for smooth user experience.
- ⏱ **Real-Time Data**: Retrieves weather data in real time from a weather API.

---