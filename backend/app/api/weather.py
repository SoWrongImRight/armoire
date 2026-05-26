from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.items import serialize
from app.core.config import settings
from app.crud import item as item_crud
from app.db.session import get_db
from app.services import weather_service

router = APIRouter(tags=["weather"])

_NOT_CONFIGURED = {
    "configured": False,
    "message": "Set OPENWEATHER_API_KEY to enable weather features.",
}


@router.get("/weather")
def current_weather(city: str = None):
    if not weather_service.is_configured():
        return _NOT_CONFIGURED
    city = city or settings.WEATHER_DEFAULT_CITY
    try:
        return {"configured": True, **weather_service.get_current_weather(city)}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Weather lookup failed: {exc}")


@router.get("/recommendations")
def recommendations(city: str = None, db: Session = Depends(get_db)):
    if not weather_service.is_configured():
        return _NOT_CONFIGURED
    city = city or settings.WEATHER_DEFAULT_CITY
    try:
        weather = weather_service.get_current_weather(city)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Weather lookup failed: {exc}")

    items = item_crud.list_items(db)
    rec = weather_service.recommend_items(items, weather["temp_c"], weather["conditions"])
    return {
        "configured": True,
        "weather": weather,
        "recommended": [serialize(i) for i in rec["chosen"]],
        "note": rec["note"],
    }
