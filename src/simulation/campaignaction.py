from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class ActionType(Enum):
    MEDIA_CAMPAIGN = "media_campaign"
    ISSUE_AD = "issue_ad"
    PHONE_BANK = "phone_bank"
    RALLY = "rally"
    DOOR_TO_DOOR = "door_to_door"
    POLICY_SPEECH = "policy_speech"
    TOWN_HALL = "town_hall"
    FUNDRAISING = "fundraising"
    VOTER_REGISTRATION = "voter_registration"
    OPPOSITION_RESEARCH = "opposition_research"
    SOCIAL_MEDIA = "social_media"
    ENDORSEMENT = "endorsement"
    SURROGATE_VISIT = "surrogate_visit"
    DEBATE_PREP = "debate_prep"
    MICRO_TARGETING = "micro_targeting"


@dataclass
class CampaignAction:
    action_type: ActionType
    week: int
    region: Optional[str] = None
    cost: float = 0.0
    intensity: float = 0.5
    description: str = ""
    issue: Optional[str] = None

    def __post_init__(self):
        self._calculate_cost()
        self._generate_description()

    def _calculate_cost(self):
        base_costs = {
            ActionType.MEDIA_CAMPAIGN: 50000,
            ActionType.ISSUE_AD: 35000,
            ActionType.PHONE_BANK: 12000,
            ActionType.RALLY: 10000,
            ActionType.DOOR_TO_DOOR: 5000,
            ActionType.POLICY_SPEECH: 15000,
            ActionType.TOWN_HALL: 8000,
            ActionType.FUNDRAISING: 2000,
            ActionType.VOTER_REGISTRATION: 3000,
            ActionType.OPPOSITION_RESEARCH: 20000,
            ActionType.SOCIAL_MEDIA: 8000,
            ActionType.ENDORSEMENT: 30000,
            ActionType.SURROGATE_VISIT: 6000,
            ActionType.DEBATE_PREP: 18000,
            ActionType.MICRO_TARGETING: 15000,
        }
        self.cost = base_costs.get(self.action_type, 10000) * (0.5 + self.intensity)

    def _generate_description(self):
        intensity_level = "intense" if self.intensity > 0.7 else "moderate" if self.intensity > 0.3 else "light"
        region_str = f" in {self.region}" if self.region else " nationally"
        action_names = {
            ActionType.MEDIA_CAMPAIGN: f"{intensity_level.capitalize()} media campaign{region_str}",
            ActionType.ISSUE_AD: f"{intensity_level.capitalize()} issue ad{region_str}",
            ActionType.PHONE_BANK: f"{intensity_level.capitalize()} phone banking blitz{region_str}",
            ActionType.RALLY: f"{intensity_level.capitalize()} rally{region_str}",
            ActionType.DOOR_TO_DOOR: f"{intensity_level.capitalize()} door-to-door canvassing{region_str}",
            ActionType.POLICY_SPEECH: f"{intensity_level.capitalize()} policy speech{region_str}",
            ActionType.TOWN_HALL: f"{intensity_level.capitalize()} town hall{region_str}",
            ActionType.FUNDRAISING: f"{intensity_level.capitalize()} fundraising effort",
            ActionType.VOTER_REGISTRATION: f"{intensity_level.capitalize()} voter registration drive{region_str}",
            ActionType.OPPOSITION_RESEARCH: f"{intensity_level.capitalize()} opposition research",
            ActionType.SOCIAL_MEDIA: f"{intensity_level.capitalize()} social media campaign{region_str}",
            ActionType.ENDORSEMENT: f"{intensity_level.capitalize()} endorsement securing",
            ActionType.SURROGATE_VISIT: f"{intensity_level.capitalize()} surrogate visit{region_str}",
            ActionType.DEBATE_PREP: f"{intensity_level.capitalize()} debate prep sprint",
            ActionType.MICRO_TARGETING: f"{intensity_level.capitalize()} micro-targeting push{region_str}",
        }
        description = action_names.get(self.action_type, "Unknown action")
        if self.issue:
            description = f"{description} on {self.issue}"
        self.description = description

ACTION_TRAIT_MAP: Dict[ActionType, str] = {
    ActionType.MEDIA_CAMPAIGN: "media_skill",
    ActionType.ISSUE_AD: "persuasion",
    ActionType.PHONE_BANK: "organization",
    ActionType.RALLY: "charisma",
    ActionType.DOOR_TO_DOOR: "organization",
    ActionType.POLICY_SPEECH: "persuasion",
    ActionType.TOWN_HALL: "authenticity",
    ActionType.FUNDRAISING: "fundraising",
    ActionType.VOTER_REGISTRATION: "organization",
    ActionType.OPPOSITION_RESEARCH: "discipline",
    ActionType.SOCIAL_MEDIA: "media_skill",
    ActionType.ENDORSEMENT: "coalition_building",
    ActionType.SURROGATE_VISIT: "coalition_building",
    ActionType.DEBATE_PREP: "debate_skill",
    ActionType.MICRO_TARGETING: "media_skill",
}


DEFAULT_DIMINISHING_RETURN_DECAY = 0.35


class ActionEffects:

    EFFECTIVENESS = {
        ActionType.MEDIA_CAMPAIGN: 0.06,
        ActionType.ISSUE_AD: 0.07,
        ActionType.PHONE_BANK: 0.08,
        ActionType.RALLY: 0.08,
        ActionType.DOOR_TO_DOOR: 0.09,
        ActionType.POLICY_SPEECH: 0.05,
        ActionType.TOWN_HALL: 0.06,
        ActionType.FUNDRAISING: 0.05,
        ActionType.VOTER_REGISTRATION: 0.0,
        ActionType.OPPOSITION_RESEARCH: -0.05,
        ActionType.SOCIAL_MEDIA: 0.04,
        ActionType.ENDORSEMENT: 0.05,
        ActionType.SURROGATE_VISIT: 0.05,
        ActionType.DEBATE_PREP: 0.04,
        ActionType.MICRO_TARGETING: 0.07,
    }

    REACH = {
        ActionType.MEDIA_CAMPAIGN: 3.0,
        ActionType.ISSUE_AD: 2.8,
        ActionType.PHONE_BANK: 1.5,
        ActionType.RALLY: 1.4,
        ActionType.DOOR_TO_DOOR: 1.1,
        ActionType.POLICY_SPEECH: 2.0,
        ActionType.TOWN_HALL: 1.2,
        ActionType.FUNDRAISING: 0.0,
        ActionType.VOTER_REGISTRATION: 1.7,
        ActionType.OPPOSITION_RESEARCH: 1.8,
        ActionType.SOCIAL_MEDIA: 2.5,
        ActionType.ENDORSEMENT: 1.6,
        ActionType.SURROGATE_VISIT: 1.0,
        ActionType.DEBATE_PREP: 1.4,
        ActionType.MICRO_TARGETING: 2.1,
    }

    EFFICIENCY = {
        ActionType.MEDIA_CAMPAIGN: 2.8,
        ActionType.ISSUE_AD: 2.6,
        ActionType.PHONE_BANK: 2.0,
        ActionType.RALLY: 1.1,
        ActionType.DOOR_TO_DOOR: 0.7,
        ActionType.POLICY_SPEECH: 2.1,
        ActionType.TOWN_HALL: 1.3,
        ActionType.FUNDRAISING: 1.0,
        ActionType.VOTER_REGISTRATION: 1.7,
        ActionType.OPPOSITION_RESEARCH: 3.3,
        ActionType.SOCIAL_MEDIA: 1.6,
        ActionType.ENDORSEMENT: 3.8,
        ActionType.SURROGATE_VISIT: 1.5,
        ActionType.DEBATE_PREP: 1.8,
        ActionType.MICRO_TARGETING: 2.3,
    }

    @staticmethod
    def get_voter_impact(action: CampaignAction, voter_engagement: float) -> float:
        base_effect = ActionEffects.EFFECTIVENESS.get(action.action_type, 0.0)
        reach_factor = 0.35 + 0.65 * max(0.0, min(1.0, voter_engagement))
        intensity_factor = 0.25 + 0.75 * action.intensity
        effect = base_effect * reach_factor * intensity_factor
        return effect

    @staticmethod
    def get_regional_spread(action: CampaignAction, source_region: Optional[str]) -> Dict[str, float]:
        if source_region:
            base = ActionEffects.REACH.get(action.action_type, 1.0) / 3.0
            return {source_region: max(0.2, min(1.0, 0.35 + base * 0.2))}
        return {}

    @staticmethod
    def get_turnout_impact(action: CampaignAction) -> float:
        turnout_actions = {
            ActionType.RALLY: 0.05,
            ActionType.DOOR_TO_DOOR: 0.06,
            ActionType.VOTER_REGISTRATION: 0.08,
            ActionType.POLICY_SPEECH: 0.03,
            ActionType.TOWN_HALL: 0.04,
            ActionType.PHONE_BANK: 0.05,
            ActionType.ISSUE_AD: 0.02,
            ActionType.SURROGATE_VISIT: 0.03,
            ActionType.DEBATE_PREP: 0.02,
            ActionType.MICRO_TARGETING: 0.05,
            ActionType.SOCIAL_MEDIA: 0.02,
        }
        base_impact = turnout_actions.get(action.action_type, 0.0)
        return base_impact * (0.45 + action.intensity)

    POPULARITY_IMPACT = {
        ActionType.MEDIA_CAMPAIGN: 0.10,
        ActionType.ISSUE_AD: 0.12,
        ActionType.PHONE_BANK: 0.08,
        ActionType.RALLY: 0.09,
        ActionType.DOOR_TO_DOOR: 0.11,
        ActionType.POLICY_SPEECH: 0.07,
        ActionType.TOWN_HALL: 0.08,
        ActionType.FUNDRAISING: 0.04,
        ActionType.VOTER_REGISTRATION: 0.06,
        ActionType.OPPOSITION_RESEARCH: -0.08,
        ActionType.SOCIAL_MEDIA: 0.09,
        ActionType.ENDORSEMENT: 0.10,
        ActionType.SURROGATE_VISIT: 0.07,
        ActionType.DEBATE_PREP: 0.06,
        ActionType.MICRO_TARGETING: 0.12,
    }

    @staticmethod
    def get_fundraising_revenue(action: CampaignAction) -> float:
        if action.action_type != ActionType.FUNDRAISING:
            return 0.0

        return 22000 + 27000 * action.intensity + 15000 * (0.5 + action.intensity)

    @staticmethod
    def get_popularity_impact(action: CampaignAction) -> float:
        base_impact = ActionEffects.POPULARITY_IMPACT.get(action.action_type, 0.0)
        intensity_factor = 0.5 + action.intensity
        total_impact = base_impact * intensity_factor
        return float(max(-0.25, min(0.25, total_impact)))
