from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import numpy as np

from simulation.campaignaction import CampaignAction, ActionType


@dataclass
class WeeklyMetrics:
    week: int
    candidate_name: str
    total_spending: float = 0.0
    actions_taken: List[CampaignAction] = field(default_factory=list)
    avg_regional_affinity: float = 0.0
    voters_reached: int = 0
    estimated_vote_share: float = 0.0
    cash_on_hand: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "week": self.week,
            "candidate": self.candidate_name,
            "spending": round(self.total_spending, 2),
            "actions": len(self.actions_taken),
            "avg_affinity": round(self.avg_regional_affinity, 3),
            "voters_reached": self.voters_reached,
            "vote_share": round(self.estimated_vote_share * 100, 1),
            "cash": round(self.cash_on_hand, 2),
        }


class CampaignState:

    def __init__(self, candidate_name: str, starting_budget: float, total_weeks: int):
        self.candidate_name = candidate_name
        self.starting_budget = starting_budget
        self.cash_on_hand = starting_budget
        self.total_weeks = total_weeks
        self.current_week = 0

        self.actions_history: List[CampaignAction] = []
        self.weekly_metrics: List[WeeklyMetrics] = []
        self.voter_affinity_changes: Dict[str, List[float]] = {}
        self.regional_affinity_history: Dict[str, List[float]] = {}

        self.is_active = True
        self.campaign_start_time = datetime.now()

    def advance_week(self):
        if self.current_week < self.total_weeks:
            self.current_week += 1
        else:
            self.is_active = False

    def record_action(self, action: CampaignAction) -> bool:
        if action.cost > self.cash_on_hand:
            return False

        self.cash_on_hand -= action.cost
        self.actions_history.append(action)
        return True

    def record_weekly_metrics(self, metrics: WeeklyMetrics):
        metrics.cash_on_hand = self.cash_on_hand
        self.weekly_metrics.append(metrics)

    def update_voter_affinity(self, voter_id: str, change: float):
        if voter_id not in self.voter_affinity_changes:
            self.voter_affinity_changes[voter_id] = []
        self.voter_affinity_changes[voter_id].append(change)

    def update_regional_affinity(self, region_name: str, avg_affinity: float):
        if region_name not in self.regional_affinity_history:
            self.regional_affinity_history[region_name] = []
        self.regional_affinity_history[region_name].append(avg_affinity)

    def get_weekly_summary(self) -> Optional[Dict]:
        if not self.weekly_metrics:
            return None
        return self.weekly_metrics[-1].to_dict()

    def get_campaign_summary(self) -> Dict:
        if not self.weekly_metrics:
            return {}

        total_spent = self.starting_budget - self.cash_on_hand
        actions_by_type = {}
        for action in self.actions_history:
            action_name = action.action_type.value
            actions_by_type[action_name] = actions_by_type.get(action_name, 0) + 1

        avg_affinity_by_region = {
            region: np.mean(affinity_list) if affinity_list else 0.0
            for region, affinity_list in self.regional_affinity_history.items()
        }

        return {
            "candidate": self.candidate_name,
            "weeks_active": self.current_week,
            "total_budget": self.starting_budget,
            "total_spent": round(total_spent, 2),
            "cash_remaining": round(self.cash_on_hand, 2),
            "total_actions": len(self.actions_history),
            "actions_by_type": actions_by_type,
            "avg_regional_affinity": avg_affinity_by_region,
            "final_vote_share": self.weekly_metrics[-1].estimated_vote_share if self.weekly_metrics else 0.0,
        }

    def get_actions_this_week(self) -> List[CampaignAction]:
        return [a for a in self.actions_history if a.week == self.current_week]

    def get_total_spending_this_week(self) -> float:
        return sum(a.cost for a in self.get_actions_this_week())

    def can_afford(self, action: CampaignAction) -> bool:
        return action.cost <= self.cash_on_hand

    def save_to_json(self, filepath: str):
        data = {
            "candidate": self.candidate_name,
            "campaign_summary": self.get_campaign_summary(),
            "weekly_metrics": [m.to_dict() for m in self.weekly_metrics],
            "timestamp": self.campaign_start_time.isoformat(),
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


class MultiCampaignTracker:

    def __init__(self, total_weeks: int):
        self.total_weeks = total_weeks
        self.current_week = 0
        self.campaigns: Dict[str, CampaignState] = {}

    def add_candidate(self, candidate_name: str, starting_budget: float):
        self.campaigns[candidate_name] = CampaignState(candidate_name, starting_budget, self.total_weeks)

    def advance_week(self):
        if self.current_week < self.total_weeks:
            self.current_week += 1
            for campaign in self.campaigns.values():
                campaign.advance_week()

    def get_candidate_campaign(self, candidate_name: str) -> Optional[CampaignState]:
        return self.campaigns.get(candidate_name)

    def get_all_summaries(self) -> Dict[str, Dict]:
        return {name: campaign.get_campaign_summary() for name, campaign in self.campaigns.items()}

    def is_campaign_complete(self) -> bool:
        return self.current_week >= self.total_weeks
