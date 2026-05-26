from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.items import serialize
from app.core.config import settings
from app.crud import item as item_crud
from app.db.session import get_db
from app.services import ai_service, weather_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/outfit")
def outfit(city: str = None, db: Session = Depends(get_db)):
    if not ai_service.is_configured():
        return {
            "configured": False,
            "message": "Set ANTHROPIC_API_KEY to enable AI outfit suggestions.",
        }

    items = item_crud.list_items(db)

    weather = None
    if weather_service.is_configured():
        try:
            weather = weather_service.get_current_weather(
                city or settings.WEATHER_DEFAULT_CITY
            )
        except Exception:  # noqa: BLE001 — weather is optional context
            weather = None

    try:
        rec = ai_service.recommend_outfit(items, weather)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"AI request failed: {exc}")

    chosen_ids = set(rec["recommended_item_ids"])
    recommended = [serialize(i) for i in items if i.id in chosen_ids]
    return {
        "configured": True,
        "rationale": rec["rationale"],
        "recommended": recommended,
        "weather": weather,
    }
