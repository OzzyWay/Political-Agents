import json
from typing import Dict

import requests
from simulation.strategies import PRESETS


def _fallback_parse(prompt: str) -> Dict[str, float]:
    text = prompt.lower()
    params = {
        "fundraising": 0.2,
        "media": 0.2,
        "ground": 0.2,
        "digital": 0.2,
        "attack": 0.2,
    }
    if "grassroots" in text or "door" in text or "ground" in text:
        params.update({"ground": 0.6, "digital": 0.1, "media": 0.1, "fundraising": 0.1, "attack": 0.1})
    if "media" in text or "tv" in text or "ad" in text:
        params.update({"media": 0.6, "digital": 0.2, "ground": 0.1, "fundraising": 0.05, "attack": 0.05})
    if "digital" in text or "social" in text or "online" in text:
        params.update({"digital": 0.6, "media": 0.2, "ground": 0.1, "fundraising": 0.05, "attack": 0.05})
    if "attack" in text or "negative" in text or "opposition" in text:
        params.update({"attack": 0.5, "media": 0.2, "digital": 0.1, "ground": 0.1, "fundraising": 0.1})
    if "fundraising" in text or "raise" in text or "cash" in text:
        params.update({"fundraising": 0.6, "digital": 0.15, "media": 0.15, "ground": 0.05, "attack": 0.05})
    total = sum(params.values())
    if total > 0:
        for k in params:
            params[k] = round(params[k] / total, 3)
    return params


def parse_prompt_to_style(prompt: str, model: str = "llama2", ollama_url: str = "http://localhost:11434") -> Dict[str, float]:
    name = (prompt or "").strip().lower()
    if name in PRESETS:
        return PRESETS[name].copy()
    try:
        req = {
            "model": model,
            "prompt": (
                "Parse the following campaign-style description and return a JSON object with numeric weights "
                "(0.0-1.0) for keys: fundraising, media, ground, digital, attack. Respond with ONLY the JSON.\n\n"
                + prompt
            ),
            "stream": False,
            "temperature": 0.3,
        }
        resp = requests.post(f"{ollama_url}/api/generate", json=req, timeout=15)
        resp.raise_for_status()
        body = resp.json().get("response", "")
        start = body.find("{")
        end = body.rfind("}")
        if start != -1 and end != -1:
            parsed = json.loads(body[start:end + 1])
            out = {k: float(parsed.get(k, 0.0)) for k in ("fundraising", "media", "ground", "digital", "attack")}
            total = sum(out.values())
            if total <= 0:
                return _fallback_parse(prompt)
            for k in out:
                out[k] = round(out[k] / total, 3)
            return out
        return _fallback_parse(prompt)
    except Exception:
        return _fallback_parse(prompt)
