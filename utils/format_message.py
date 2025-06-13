import datetime
from collections import defaultdict

WEATHER_ICONS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️",
}


def get_weather_emoji(desc: str) -> str:
    desc = desc.lower()
    for key, emoji in WEATHER_ICONS.items():
        if key in desc:
            return emoji
    return "🌡️"


def group_forecasts_by_day(forecasts: list, max_intervals: int) -> dict:
    grouped = defaultdict(list)
    for f in forecasts[:max_intervals]:
        date = f["dt_txt"].split()[0]
        grouped[date].append(f)
    return grouped


def format_forecast_message(city: str, grouped: dict, days: int) -> str:
    result = f"🌤 <b>Weather forecast for {city} (next {days} day(s)):</b>\n"
    for date, entries in grouped.items():
        result += f"\n\n<b>{date}</b>\n"
        for f in entries:
            time = f["dt_txt"].split()[1][:5]
            temp = f["main"]["temp"]
            feels = f["main"].get("feels_like", temp)
            desc = f["weather"][0]["description"].capitalize()
            wind = f["wind"]["speed"]
            humidity = f["main"]["humidity"]
            icon = get_weather_emoji(desc)
            result += (
                f"{time} {icon} {desc}, "
                f"{temp:.1f}°C (feels {feels:.1f}°C), "
                f"💨 {wind} m/s, 💧 {humidity}%\n"
            )
    return result


def format_hourly_message(city: str, forecasts: list) -> str:
    result = f"🕒 <b>Hourly forecast for {city} (next 24h):</b>\n"
    for f in forecasts[:8]:
        dt_txt = f["dt_txt"]
        time = dt_txt.split(" ")[1][:5]
        temp = f["main"]["temp"]
        feels = f["main"].get("feels_like", temp)
        desc = f["weather"][0]["description"].capitalize()
        wind = f["wind"]["speed"]
        humidity = f["main"]["humidity"]
        icon = get_weather_emoji(desc)
        result += (
            f"\n<b>{time}</b> {icon} {desc}, "
            f"{temp:.1f}°C (feels {feels:.1f}°C), "
            f"💨 {wind} m/s, 💧 {humidity}%"
        )
    return result


def format_weather_message(data: dict) -> str:
    import datetime
    city_name = data.get("name", "")
    temp = data.get("main", {}).get("temp")
    feels = data.get("main", {}).get("feels_like", temp)
    desc = data.get("weather", [{}])[0].get("description", "").capitalize()
    wind = data.get("wind", {}).get("speed")
    humidity = data.get("main", {}).get("humidity")
    pressure = data.get("main", {}).get("pressure")
    dt = data.get("dt")
    icon = get_weather_emoji(desc)
    time_str = (
        datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
        if dt else ""
    )

    return (
        f"{icon} <b>{city_name}</b>\n"
        f"🕒 <b>Time:</b> {time_str}\n"
        f"🌡️ <b>Temperature:</b> {temp:.1f}°C (feels {feels:.1f}°C)\n"
        f"☁️ <b>Weather:</b> {desc}\n"
        f"💨 <b>Wind:</b> {wind} m/s\n"
        f"💧 <b>Humidity:</b> {humidity}%\n"
        f"🔽 <b>Pressure:</b> {pressure} hPa"
    )


def format_air_quality_message(city: str, air_info: dict) -> str:
    aqi = air_info["main"]["aqi"]
    components = air_info.get("components", {})
    aqi_text = {
        1: "Good 🟢",
        2: "Fair 🟡",
        3: "Moderate 🟠",
        4: "Poor 🟣",
        5: "Very Poor 🔴"
    }.get(aqi, "Unknown")

    return (
        f"🌬️ <b>Air quality in {city}:</b>\n"
        f"AQI: <b>{aqi}</b> ({aqi_text})\n"
        f"• CO: {components.get('co', '-')} μg/m³\n"
        f"• NO: {components.get('no', '-')} μg/m³\n"
        f"• NO₂: {components.get('no2', '-')} μg/m³\n"
        f"• O₃: {components.get('o3', '-')} μg/m³\n"
        f"• SO₂: {components.get('so2', '-')} μg/m³\n"
        f"• PM2.5: {components.get('pm2_5', '-')} μg/m³\n"
        f"• PM10: {components.get('pm10', '-')} μg/m³\n"
        f"• NH₃: {components.get('nh3', '-')} μg/m³"
    )


def format_details_message(data: dict) -> str:
    city_name = data.get("name", "")
    country = data.get("sys", {}).get("country", "")
    coord = data.get("coord", {})
    temp = data.get("main", {}).get("temp")
    feels = data.get("main", {}).get("feels_like", temp)
    temp_min = data.get("main", {}).get("temp_min")
    temp_max = data.get("main", {}).get("temp_max")
    humidity = data.get("main", {}).get("humidity")
    pressure = data.get("main", {}).get("pressure")
    sea_level = data.get("main", {}).get("sea_level")
    grnd_level = data.get("main", {}).get("grnd_level")
    desc = data.get("weather", [{}])[0].get("description", "").capitalize()
    icon = get_weather_emoji(desc)
    wind = data.get("wind", {})
    clouds = data.get("clouds", {}).get("all")
    visibility = data.get("visibility")
    dt = data.get("dt")
    time_str = (
        datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
        if dt else ""
    )
    sunrise = data.get("sys", {}).get("sunrise")
    sunset = data.get("sys", {}).get("sunset")
    timezone = data.get("timezone", 0)

    def local_time(ts):
        if not ts:
            return "-"
        return (datetime.datetime.utcfromtimestamp(ts + timezone)
                .strftime('%H:%M'))

    return (
        f"{icon} <b>Detailed weather for {city_name}, {country}</b>\n"
        f"🕒 <b>Time:</b> {time_str}\n"
        f"🌍 <b>Coordinates:</b> {coord.get('lat', '-')}, {coord.get('lon', '-')}\n"
        f"☁️ <b>Weather:</b> {desc}\n"
        f"🌡️ <b>Temperature:</b> {temp:.1f}°C (feels {feels:.1f}°C)\n"
        f"🔼 <b>Max:</b> {temp_max:.1f}°C   🔽 <b>Min:</b> {temp_min:.1f}°C\n"
        f"💧 <b>Humidity:</b> {humidity}%\n"
        f"🔽 <b>Pressure:</b> {pressure} hPa\n"
        f"🌊 <b>Sea level:</b> {sea_level if sea_level else '-'} hPa\n"
        f"⛰️ <b>Ground level:</b> {grnd_level if grnd_level else '-'} hPa\n"
        f"🌬️ <b>Wind:</b> {wind.get('speed', '-')} m/s, "
        f"deg: {wind.get('deg', '-')}, gust: {wind.get('gust', '-')}\n"
        f"🌫️ <b>Cloudiness:</b> {clouds}%\n"
        f"👁️ <b>Visibility:</b> {visibility} m\n"
        f"🌅 <b>Sunrise:</b> {local_time(sunrise)}   "
        f"🌇 <b>Sunset:</b> {local_time(sunset)}\n"
    )


def format_sunrise_sunset_message(data: dict) -> str:
    city_name = data.get("name", "")
    country = data.get("sys", {}).get("country", "")
    sunrise = data.get("sys", {}).get("sunrise")
    sunset = data.get("sys", {}).get("sunset")
    timezone = data.get("timezone", 0)

    def local_time(ts):
        if not ts:
            return "-"
        return (datetime.datetime.utcfromtimestamp(ts + timezone)
                .strftime('%H:%M'))

    return (
        f"🌅 <b>Sunrise and Sunset in {city_name}, {country}</b>\n"
        f"🌞 <b>Sunrise:</b> {local_time(sunrise)}\n"
        f"🌇 <b>Sunset:</b> {local_time(sunset)}"
    )


def format_wind_message(data: dict) -> str:
    city_name = data.get("name", "")
    country = data.get("sys", {}).get("country", "")
    wind = data.get("wind", {})
    speed = wind.get("speed", "-")
    deg = wind.get("deg", "-")
    gust = wind.get("gust", "-")

    def deg_to_dir(deg):
        dirs = [
            "N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"
        ]
        if deg == "-":
            return "-"
        ix = int((deg + 22.5) // 45)
        return dirs[ix % 8]

    dir_str = deg_to_dir(deg) if deg != "-" else "-"

    return (
        f"💨 <b>Wind in {city_name}, {country}</b>\n"
        f"🌬️ <b>Speed:</b> {speed} m/s\n"
        f"🧭 <b>Direction:</b> {deg}° ({dir_str})\n"
        f"💨 <b>Gusts:</b> {gust if gust != '-' else 'No data'}"
    )


def get_time_text(time: str) -> str:
    return f"\n• <b>Time:</b> {time}" if time else ""
