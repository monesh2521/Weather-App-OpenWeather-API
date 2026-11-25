"""OpenWeather API client with short-lived caching and friendly errors."""
import os
import time
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_KEY", "").strip()
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
CACHE_SECONDS = 600
_cache: dict[tuple[str, str], tuple[float, dict[str, Any]]] = {}


class WeatherError(Exception):
    """An error that can be shown directly to the user."""


def _request_json(url: str, city: str) -> dict[str, Any]:
    if not API_KEY:
        raise WeatherError(
            "OpenWeather API key is missing. Copy .env.example to .env "
            "and add your key as OPENWEATHER_KEY=your_key_here."
        )

    cache_key = (url, city.casefold())
    cached = _cache.get(cache_key)
    if cached and time.time() - cached[0] < CACHE_SECONDS:
        return cached[1]

    try:
        response = requests.get(
            url,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
    except requests.exceptions.Timeout as exc:
        raise WeatherError("The request timed out. Please try again.") from exc
    except requests.exceptions.RequestException as exc:
        raise WeatherError(
            "Network problem. Check your internet connection and try again."
        ) from exc

    if response.status_code == 404:
        raise WeatherError(f"City '{city}' was not found. Check the spelling.")
    if response.status_code == 401:
        raise WeatherError(
            "OpenWeather rejected the API key (401). Check your .env key. "
            "A newly created key may take a little time to activate."
        )
    if response.status_code == 429:
        raise WeatherError("API request limit reached. Please wait and try again.")
    if response.status_code != 200:
        raise WeatherError(f"Weather service error: HTTP {response.status_code}.")

    try:
        data = response.json()
    except ValueError as exc:
        raise WeatherError("The weather service returned invalid JSON.") from exc

    _cache[cache_key] = (time.time(), data)
    return data


def get_current_weather(city: str) -> dict[str, Any]:
    """Return current weather fields for a city."""
    data = _request_json(CURRENT_URL, city)
    main = data.get("main") or {}
    weather_list = data.get("weather") or [{}]
    wind = data.get("wind") or {}
    return {
        "city": data.get("name", city),
        "country": (data.get("sys") or {}).get("country", ""),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "description": (weather_list[0] or {}).get("description", "Not available").title(),
        "wind_speed": wind.get("speed"),
        "icon": (weather_list[0] or {}).get("icon", ""),
    }


def get_five_day_forecast(city: str) -> list[dict[str, Any]]:
    """Pick the forecast closest to 12:00 for each of the next five dates."""
    data = _request_json(FORECAST_URL, city)
    entries = data.get("list") or []
    by_date: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        date_text = (entry.get("dt_txt") or "").split(" ")[0]
        if date_text:
            by_date.setdefault(date_text, []).append(entry)

    result = []
    for date_text in sorted(by_date)[:5]:
        # Prefer noon; if no noon slot exists, use the available entry nearest noon.
        chosen = min(
            by_date[date_text],
            key=lambda item: abs(
                datetime.strptime(item.get("dt_txt", date_text + " 12:00:00"),
                                  "%Y-%m-%d %H:%M:%S").hour - 12
            ),
        )
        main = chosen.get("main") or {}
        weather = (chosen.get("weather") or [{}])[0] or {}
        result.append({
            "date": datetime.strptime(date_text, "%Y-%m-%d").strftime("%a, %d %b"),
            "temperature": main.get("temp"),
            "description": weather.get("description", "Not available").title(),
            "humidity": main.get("humidity"),
        })
    return result
