"""Standardized preference/weight containers.

Preferences use the -1.0..+1.0 scale described in the improvement spec:
    -1.0 = strongly favors position A
     0.0 = neutral
    +1.0 = strongly favors position B

Weights (issue importance) use a separate 0.0..1.0 scale and are never
mixed with the preference scale.

Both containers clamp their values on construction so a bad upstream value
(bad config, unclamped noise, etc.) can never silently propagate through
the rest of the simulation as an out-of-range number.
"""
from dataclasses import dataclass

from simulation.mathutils import clamp

POLICY_KEYS = [
    "economy",
    "tax",
    "healthcare",
    "education",
    "immigration",
    "environment",
    "crime",
    "government_size",
    "foreign_policy",
    "infrastructure",
]


@dataclass
class Preferences:
    economy: float
    tax: float
    healthcare: float
    education: float
    immigration: float
    environment: float
    crime: float
    government_size: float
    foreign_policy: float
    infrastructure: float

    def __post_init__(self):
        for key in POLICY_KEYS:
            setattr(self, key, clamp(float(getattr(self, key)), -1.0, 1.0))

    def as_dict(self):
        return {key: getattr(self, key) for key in POLICY_KEYS}


@dataclass
class Weights:
    economy: float
    tax: float
    healthcare: float
    education: float
    immigration: float
    environment: float
    crime: float
    government_size: float
    foreign_policy: float
    infrastructure: float

    def __post_init__(self):
        for key in POLICY_KEYS:
            setattr(self, key, clamp(float(getattr(self, key)), 0.0, 1.0))

    def as_dict(self):
        return {key: getattr(self, key) for key in POLICY_KEYS}
