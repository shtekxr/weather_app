import httpx
from typing import Dict


async def get_weather(city: str, search_history: Dict[str, int]):
    """
    Координаты городов
    """
    city_coordinates = {
        "Berlin": {"latitude": 52.52, "longitude": 13.41},
        "Moscow": {"latitude": 55.75, "longitude": 37.62},
        "New York": {"latitude": 40.71, "longitude": -74.01},
        "Tokyo": {"latitude": 35.68, "longitude": 139.76},
        "Paris": {"latitude": 48.85, "longitude": 2.35}
    }

    if city not in city_coordinates:
        return {"error": "City not found"}

    coordinates = city_coordinates[city]
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={coordinates['latitude']}&longitude="
           f"{coordinates['longitude']}&hourly=temperature_2m")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    """
    Форматирование данных для удобства пользователя
    """
    weather_info = []
    for time, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]):
        weather_info.append({"time": time, "temperature": temp})

    """
    Возвращаем прогноз за сутки
    """
    return {
        "search_history": search_history,
        "city": city,
        "weather": weather_info[:24]
    }


async def autocomplete_city(query: str):
    cities = ["Berlin", "Paris", "New York", "Moscow", "Tokyo"]
    suggestions = [city for city in cities if query.lower() in city.lower()]
    return suggestions
