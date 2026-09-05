"""
Sloth AI - Compliance Agent
Classifies scraped regulatory updates by jurisdiction and severity, and
generates an actionable alert for each — matching the "Sloth AI Alert"
card shown in the product demo (jurisdiction flag, description, action).
"""
import json
import os
import re

from groq import AsyncGroq

MODEL = "openai/gpt-oss-120b"

_CLIENT = None


def _client():
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
    return _CLIENT


async def _json(system, user):
    r = await _client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system + "\n\nRespond ONLY with valid JSON. No markdown."},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    raw = r.choices[0].message.content.strip()
    clean = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        m = re.search(r"[\[{].*[\]}]", clean, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        return {"raw": raw}


async def analyze_updates(scraped_data):
    """
    Takes raw scraped regulatory headlines and returns a list of
    structured, actionable compliance alerts.
    """
    items = scraped_data.get("items", [])
    if not items:
        return []

    result = await _json(
        "You are Sloth AI's Compliance Agent. You monitor regulatory and "
        "tax changes across jurisdictions for a multinational client base.\n"
        "For each item given, produce an alert. Return a JSON array, one "
        "object per item:\n"
        "[{\"jurisdiction\": \"<country/region>\", "
        "\"headline\": \"<original headline>\", "
        "\"severity\": \"LOW|MEDIUM|HIGH|CRITICAL\", "
        "\"description\": \"<2-3 sentence plain-language explanation of what "
        "changed and who it affects>\", "
        "\"recommended_action\": \"<one concrete next step>\", "
        "\"deadline_days\": <int or null if no clear deadline>}]",
        f"Items: {json.dumps(items)}",
    )

    if isinstance(result, list):
        return result
    return []
