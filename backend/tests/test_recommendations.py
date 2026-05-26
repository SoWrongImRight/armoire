from types import SimpleNamespace

from app.services.weather_service import recommend_items

WARDROBE = [
    SimpleNamespace(id=1, name="Wool Coat", category="outerwear", season="winter"),
    SimpleNamespace(id=2, name="Tee", category="top", season="summer"),
    SimpleNamespace(id=3, name="Flannel", category="top", season="fall"),
    SimpleNamespace(id=4, name="Jeans", category="bottom", season="all"),
    SimpleNamespace(id=5, name="Sneakers", category="shoes", season="all"),
]


def test_cold_includes_outerwear():
    rec = recommend_items(WARDROBE, 2, "Snow")
    assert "outerwear" in {i.category for i in rec["chosen"]}


def test_hot_excludes_outerwear():
    rec = recommend_items(WARDROBE, 28, "Clear")
    assert "outerwear" not in {i.category for i in rec["chosen"]}


def test_rain_note_present():
    rec = recommend_items(WARDROBE, 12, "Rain")
    assert rec["note"] and "waterproof" in rec["note"].lower()


def test_no_temperature_is_safe():
    rec = recommend_items(WARDROBE, None, "")
    assert isinstance(rec["chosen"], list)
