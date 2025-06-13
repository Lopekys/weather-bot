import time

import aiohttp

_weather_cache = {}
_forecast_cache = {}
_geo_cache = {}
_air_cache = {}

CACHE_TTL = 300


async def get_current_weather_full(city: str, api_key: str):
    """
    Get the full JSON response for current weather conditions for a city from OpenWeather API 2.5.

    Args:
        city (str): Name of the city (in English or transliterated).
        api_key (str): Your OpenWeather API key.

    Returns:
        dict: JSON data with current weather conditions, or None if an error occurred.
    """
    now = time.time()
    city_key = city.lower()
    cache_data = _weather_cache.get(city_key)
    if cache_data and now - cache_data["timestamp"] < CACHE_TTL:
        return cache_data["data"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            _weather_cache[city_key] = {
                "timestamp": now,
                "data": data
            }
            return data


async def get_forecast_json(city: str, api_key: str):
    """
    Get the full JSON response for a 5-day / 3-hour weather forecast for a city from OpenWeather API 2.5.
    Returns dict or None if error.
    """
    now = time.time()
    city_key = city.lower()
    cache_data = _forecast_cache.get(city_key)
    if cache_data and now - cache_data["timestamp"] < CACHE_TTL:
        return cache_data["data"]

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={api_key}&units=metric&lang=en"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            if resp.status != 200:
                print(f"OpenWeather FORECAST error: status={resp.status}, text={text}")
                return None
            data = await resp.json()
            if data.get("cod") != "200":
                print(f"OpenWeather FORECAST error: cod={data.get('cod')}, message={data.get('message')}, city={city}")
                return None
            if "list" not in data:
                print(f"OpenWeather FORECAST: no 'list' in response, city={city}, data={data}")
                return None
            _forecast_cache[city_key] = {
                "timestamp": now,
                "data": data
            }
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
    now = time.time()
    coord_key = f"{lat},{lon}"
    cache_data = _air_cache.get(coord_key)
    if cache_data and now - cache_data["timestamp"] < CACHE_TTL:
        return cache_data["data"]

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            _air_cache[coord_key] = {
                "timestamp": now,
                "data": data
            }
            return data
