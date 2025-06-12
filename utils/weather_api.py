import aiohttp


async def get_current_weather_full(city: str, api_key: str):
    """
    Gets the full JSON of the current weather from the OpenWeather API 2.5 by city name.
    Returns dict (the API response) or None on error.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data