import requests

from app.core.config import settings

OWM_URL = "https://api.openweathermap.org/data/2.5/weather"


def is_configured() -> bool:
    return bool(settings.OPENWEATHER_API_KEY)


def get_current_weather(city: str) -> dict:
    resp = requests.get(
        OWM_URL,
        params={
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    weather = (data.get("weather") or [{}])[0]
    return {
        "city": data.get("name", city),
        "temp_c": data.get("main", {}).get("temp"),
        "conditions": weather.get("main", "Unknown"),
        "description": weather.get("description", ""),
    }


def recommend_items(items, temp_c, conditions):
    """Pick one item per relevant category based on temperature and weather."""
    if temp_c is None:
        seasons, wanted = {"all"}, ["top", "bottom", "shoes"]
    elif temp_c <= 5:
        seasons = {"winter", "all"}
        wanted = ["outerwear", "top", "bottom", "shoes", "accessory"]
    elif temp_c <= 15:
        seasons = {"fall", "winter", "all"}
        wanted = ["outerwear", "top", "bottom", "shoes"]
    elif temp_c <= 24:
        seasons = {"spring", "fall", "all"}
        wanted = ["top", "bottom", "shoes"]
    else:
        seasons = {"summer", "spring", "all"}
        wanted = ["top", "bottom", "shoes"]

    chosen = []
    for category in wanted:
        match = next(
            (
                i
                for i in items
                if i.category == category and (i.season is None or i.season in seasons)
            ),
            None,
        )
        if match:
            chosen.append(match)

    note = None
    if conditions and "rain" in conditions.lower():
        note = "Rain expected — bring a waterproof layer."
    return {"chosen": chosen, "note": note}
