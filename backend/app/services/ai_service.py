import json

import anthropic

from app.core.config import settings

# Stable instructions — eligible for prompt caching. (In practice this prefix
# is well under the model's minimum cacheable size, so it won't actually cache
# until the prompt grows; the cache_control marker is correct either way.)
SYSTEM_PROMPT = (
    "You are Armoire's personal stylist. Given a user's wardrobe and optional "
    "weather, choose a single coherent outfit using ONLY the provided items. "
    "Prefer items suited to the weather and season, and pick at most one item "
    "per category. Respond with a JSON object and nothing else, exactly:\n"
    '{"recommended_item_ids": [<int>, ...], "rationale": "<one or two sentences>"}\n'
    "If the wardrobe is empty, return an empty list and say no items are available."
)


def is_configured() -> bool:
    return bool(settings.ANTHROPIC_API_KEY)


def build_user_prompt(items, weather=None) -> str:
    lines = ["Wardrobe items:"]
    for item in items:
        parts = [f"id={item.id}", f"name={item.name}", f"category={item.category}"]
        if item.brand:
            parts.append(f"brand={item.brand}")
        if item.season:
            parts.append(f"season={item.season}")
        if item.color:
            parts.append(f"color={item.color}")
        lines.append("- " + ", ".join(parts))
    if not items:
        lines.append("(none)")
    if weather:
        lines.append("")
        lines.append(
            f"Weather: {weather.get('temp_c')}°C, "
            f"{weather.get('conditions')} in {weather.get('city')}."
        )
    lines.append("")
    lines.append("Suggest one outfit.")
    return "\n".join(lines)


def recommend_outfit(items, weather=None) -> dict:
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": build_user_prompt(items, weather)}],
    )
    text = next((b.text for b in response.content if b.type == "text"), "")
    return parse_recommendation(text)


def parse_recommendation(text: str) -> dict:
    try:
        data = json.loads(text)
        ids = [int(x) for x in data.get("recommended_item_ids", [])]
        rationale = str(data.get("rationale", "")).strip()
    except (ValueError, TypeError, json.JSONDecodeError):
        ids, rationale = [], text.strip()
    return {"recommended_item_ids": ids, "rationale": rationale}
