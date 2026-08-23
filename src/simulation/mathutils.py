from __future__ import annotations

from typing import Dict, Iterable

import numpy as np


def clamp(value: float, lo: float, hi: float) -> float:
    if value != value:
        return lo
    return max(lo, min(hi, value))


def weighted_average(values: Iterable[float], weights: Iterable[float]) -> float:
    values = list(values)
    weights = list(weights)

    if not values:
        return 0.0

    total_weight = sum(weights)
    if total_weight <= 0:
        return float(np.mean(values))

    return float(sum(v * w for v, w in zip(values, weights)) / total_weight)


def stable_softmax(scores: Dict[str, float], temperature: float = 0.15) -> Dict[str, float]:
    if not scores:
        return {}

    temperature = max(1e-6, float(temperature))
    keys = list(scores.keys())
    raw = np.array([scores[k] for k in keys], dtype=float) / temperature

    raw = raw - np.max(raw)
    exp_values = np.exp(raw)
    total = float(np.sum(exp_values))

    if total <= 0.0 or not np.isfinite(total):
        uniform = 1.0 / len(keys)
        return {k: uniform for k in keys}

    return {k: float(v) / total for k, v in zip(keys, exp_values)}


def diminishing_return(previous_uses: int, decay_factor: float = 0.35) -> float:
    previous_uses = max(0, int(previous_uses))
    decay_factor = max(0.0, float(decay_factor))
    return 1.0 / (1.0 + previous_uses * decay_factor)
