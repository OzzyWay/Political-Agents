from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

import numpy as np

from simulation.mathutils import clamp


class EventType(Enum):
    DEBATE = "debate"
    SCANDAL = "scandal"
    ENDORSEMENT = "endorsement"
    ECONOMIC_CHANGE = "economic_change"
    POLICY_ANNOUNCEMENT = "policy_announcement"
    VIRAL_MOMENT = "viral_moment"
    GAFFE = "gaffe"
    NEWS_CYCLE = "news_cycle"
    NATURAL_DISASTER = "natural_disaster"


@dataclass
class CampaignEvent:
    event_type: EventType
    week: int
    candidate_name: str
    region: Optional[str] = None
    affinity_delta: float = 0.0
    popularity_delta: float = 0.0
    turnout_delta: float = 0.0
    description: str = ""

    def __post_init__(self):
        if not self.description:
            scope = f" in {self.region}" if self.region else " (national)"
            self.description = f"{self.event_type.value.replace('_', ' ').title()}{scope}: {self.candidate_name}"

    def _affected_regions(self, world):
        if self.region:
            return [r for r in world.regions if r.name == self.region]
        return world.regions

    def apply(self, world, party_by_candidate_name: Dict[str, object]) -> Dict:
        summary = {"description": self.description, "voters_affected": 0}

        party = party_by_candidate_name.get(self.candidate_name)
        if party is not None and self.popularity_delta:
            party.adjust_popularity(self.popularity_delta)
            summary["popularity_after"] = party.popularity

        for region in self._affected_regions(world):
            for voter in region.voter_list:
                if self.affinity_delta:
                    current = voter.candidate_affinity.get(self.candidate_name, 0.5)
                    jitter = self.affinity_delta * (0.7 + 0.6 * np.random.random())
                    voter.candidate_affinity[self.candidate_name] = clamp(current + jitter, 0.0, 1.0)
                if self.turnout_delta:
                    voter.turnout_probability = clamp(
                        voter.turnout_probability + self.turnout_delta, 0.0, 1.0
                    )
                summary["voters_affected"] += 1

        return summary

    def to_dict(self) -> Dict:
        return {
            "event_type": self.event_type.name,
            "week": int(self.week),
            "candidate_name": self.candidate_name,
            "region": self.region,
            "affinity_delta": float(self.affinity_delta),
            "popularity_delta": float(self.popularity_delta),
            "turnout_delta": float(self.turnout_delta),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CampaignEvent":
        et = EventType[data.get("event_type")] if data.get("event_type") in EventType.__members__ else EventType.NEWS_CYCLE
        return cls(
            event_type=et,
            week=int(data.get("week", 1)),
            candidate_name=data.get("candidate_name", ""),
            region=data.get("region"),
            affinity_delta=float(data.get("affinity_delta", 0.0)),
            popularity_delta=float(data.get("popularity_delta", 0.0)),
            turnout_delta=float(data.get("turnout_delta", 0.0)),
            description=data.get("description", ""),
        )
