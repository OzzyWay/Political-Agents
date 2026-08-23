"""Lightweight per-voter memory of campaign interactions.

Scandals, ads, speeches, and other events shouldn't just nudge a voter's
affinity and vanish -- they should linger for a while and then fade. This
module is intentionally tiny: a capped list of recent (candidate, issue,
action, effect, week) records plus an exponential-decay lookup, so it stays
cheap even across tens of thousands of voters.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

MAX_MEMORIES_PER_VOTER = 12
DEFAULT_HALF_LIFE_WEEKS = 3.0


@dataclass
class CampaignMemory:
    candidate: str
    action: str
    effect: float
    week: int
    issue: Optional[str] = None


class VoterMemory:
    def __init__(self):
        self.memories: List[CampaignMemory] = []

    def remember(self, memory: CampaignMemory):
        self.memories.append(memory)
        if len(self.memories) > MAX_MEMORIES_PER_VOTER:
            self.memories.pop(0)

    def decayed_effect(self, current_week: int, candidate: Optional[str] = None,
                        half_life_weeks: float = DEFAULT_HALF_LIFE_WEEKS) -> float:
        half_life_weeks = max(0.1, half_life_weeks)
        total = 0.0
        for memory in self.memories:
            if candidate is not None and memory.candidate != candidate:
                continue
            age_weeks = max(0, current_week - memory.week)
            decay = 0.5 ** (age_weeks / half_life_weeks)
            total += memory.effect * decay
        return total
