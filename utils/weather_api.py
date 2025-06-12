import aiohttp


async def get_current_weather_full(city: str, api_key: str):
    """
    Get the full JSON response for current weather conditions for a city from OpenWeather API 2.5.

    Args:
        city (str): Name of the city (in English or transliterated).
        api_key (str): Your OpenWeather API key.

    Returns:
        dict: JSON data with current weather conditions, or None if an error occurred.
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


async def get_forecast_json(city: str, api_key: str):
    """
    Get the full JSON response for a 5-day / 3-hour weather forecast for a city from OpenWeather API 2.5.

    Args:
        city (str): Name of the city (in English or transliterated).
        api_key (str): Your OpenWeather API key.

    Returns:
        dict: JSON data with forecast information, or None if an error occurred.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={api_key}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data


async def get_city_coordinates(city: str, api_key: str):
    """
       Get the latitude and longitude of a city using the OpenWeather Geocoding API.

       Args:
           city (str): The name of the city to search for.
           api_key (str): Your OpenWeather API key.

       Returns:
           tuple: (lat, lon) as floats if found, otherwise (None, None).
       """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None, None
            data = await resp.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                return lat, lon
            return None, None


async def get_air_quality(lat: float, lon: float, api_key: str):
    """
        Get air quality data for a specific location using the OpenWeather Air Pollution API.

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
            api_key (str): Your OpenWeather API key.

        Returns:
            dict: Air quality data from the API response, or None if an error occurred.
        """
    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data
