from typing import Dict

def _norm(d: Dict[str, float]) -> Dict[str, float]:
    total = sum(d.values())
    if total <= 0:
        return {k: 0.0 for k in d}
    return {k: round(v / total, 3) for k, v in d.items()}

PRESETS = {
    "balanced": _norm({"fundraising": 0.2, "media": 0.25, "ground": 0.25, "digital": 0.2, "attack": 0.1}),
    "grassroots": _norm({"fundraising": 0.1, "media": 0.05, "ground": 0.6, "digital": 0.15, "attack": 0.1}),
    "media_blitz": _norm({"fundraising": 0.15, "media": 0.6, "ground": 0.05, "digital": 0.15, "attack": 0.05}),
    "digital_first": _norm({"fundraising": 0.1, "media": 0.2, "ground": 0.1, "digital": 0.55, "attack": 0.05}),
    "attack_heavy": _norm({"fundraising": 0.1, "media": 0.3, "ground": 0.05, "digital": 0.15, "attack": 0.4}),
    "fundraising_focused": _norm({"fundraising": 0.7, "media": 0.1, "ground": 0.05, "digital": 0.1, "attack": 0.05}),
}
