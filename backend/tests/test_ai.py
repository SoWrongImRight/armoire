from types import SimpleNamespace

from app.services.ai_service import build_user_prompt, parse_recommendation


def test_parse_valid_json():
    rec = parse_recommendation(
        '{"recommended_item_ids": [1, 2], "rationale": "Cozy and warm."}'
    )
    assert rec["recommended_item_ids"] == [1, 2]
    assert rec["rationale"] == "Cozy and warm."


def test_parse_malformed_falls_back_to_text():
    rec = parse_recommendation("not json at all")
    assert rec["recommended_item_ids"] == []
    assert rec["rationale"] == "not json at all"


def test_build_user_prompt_includes_items_and_weather():
    items = [
        SimpleNamespace(id=1, name="Tee", category="top", brand=None, season="summer", color="white"),
    ]
    prompt = build_user_prompt(items, {"temp_c": 28, "conditions": "Clear", "city": "Orlando"})
    assert "id=1" in prompt
    assert "category=top" in prompt
    assert "Orlando" in prompt


def test_build_user_prompt_handles_empty_wardrobe():
    prompt = build_user_prompt([], None)
    assert "(none)" in prompt
