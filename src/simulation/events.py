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
