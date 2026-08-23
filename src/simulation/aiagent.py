import json
import requests
from typing import List, Dict, Optional, Tuple
from simulation.campaignaction import CampaignAction, ActionType, ActionEffects
from simulation.campaignstate import CampaignState


def top_issue(world_state: Dict) -> Optional[str]:
    issues = world_state.get("issues", {})
    if not issues:
        return None
    return max(issues.items(), key=lambda item: item[1].get("importance", 0.0))[0]


class CampaignAdvisor:
    def __init__(self, model: str = "llama2", ollama_url: str = "http://localhost:11434"):
        self.model = model
        self.ollama_url = ollama_url
        self.candidate_name = None

    def set_candidate(self, candidate_name: str):
        self.candidate_name = candidate_name

    def _request_model_output(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could not connect to Ollama at {self.ollama_url}. Make sure Ollama is running.")
        except Exception as e:
            raise RuntimeError(f"Error calling Ollama: {e}")

    def build_status_prompt(self, campaign: CampaignState, world_state: Dict) -> str:
        context = f"""
        CAMPAIGN STATUS FOR {campaign.candidate_name}:
        - Week: {campaign.current_week}/{campaign.total_weeks}
        - Cash on hand: ${campaign.cash_on_hand:,.0f}
        - Starting budget: ${campaign.starting_budget:,.0f}
        - National affinity: {world_state.get('national_affinity', {}).get(campaign.candidate_name, 0.0):.1%}

        CURRENT POLLING (regional affinity, by candidate):
        {json.dumps(world_state.get('regional_affinity', {}), indent=2)}

        REGIONAL TURNOUT (share of eligible voters expected to vote):
        {json.dumps(world_state.get('regional_turnout', {}), indent=2)}

        PERSUADABLE VOTERS (share of each region not yet strongly attached
        to any candidate -- these are the voters worth targeting):
        {json.dumps(world_state.get('regional_persuadable', {}), indent=2)}

        ISSUE IMPORTANCE (how much the electorate cares about each issue,
        0=nobody cares, 1=everyone cares a lot):
        {json.dumps(world_state.get('issues', {}), indent=2)}

        RECENT ACTIONS:
        {self.summarize_recent_actions(campaign)}

        AVAILABLE ACTIONS:
        - MEDIA_CAMPAIGN: $50k-100k, broad reach, strong general persuasion
        - ISSUE_AD: $35k-70k, targeted message emphasis with fast signal value
        - PHONE_BANK: $12k-24k, direct persuasion and turnout lift
        - RALLY: $10k-20k, high energy, strong enthusiasm boost
        - DOOR_TO_DOOR: $5k-10k, personal touch, highest persuasion on local voters
        - POLICY_SPEECH: $15k-30k, appeals to interested voters and policy-focused audiences
        - TOWN_HALL: $8k-16k, high engagement and local trust building
        - FUNDRAISING: $2k-4k to start, but brings in significant new cash and rebuilds the war chest
        - VOTER_REGISTRATION: $3k-6k, increase turnout, regional and mobilization focused
        - SOCIAL_MEDIA: $8k-16k, younger voters, broad digital reach
        - OPPOSITION_RESEARCH: $20k-40k, attack opponent, regional effect and negative persuasion
        - ENDORSEMENT: $30k-60k, credibility boost from endorsers and coalitions
        - SURROGATE_VISIT: $6k-12k, local credibility and regional trust-building
        - DEBATE_PREP: $18k-36k, helps with persuasion after debates or key moments
        - MICRO_TARGETING: $15k-30k, precision persuasion on likely supporters and persuadables

        YOUR GOAL:
        Maximize your candidate's vote share by strategically allocating limited campaign resources.
        Consider regional strengths/weaknesses, opponent movements, and ROI of different actions.
        """
        return context

    def summarize_recent_actions(self, campaign: CampaignState) -> str:
        recent = campaign.get_actions_this_week()
        if not recent:
            return "No actions taken this week yet."

        formatted = []
        for action in recent:
            formatted.append(f"- {action.description} (${action.cost:,.0f})")
        return "\n".join(formatted)

    def decide_actions(
        self,
        campaign: CampaignState,
        world_state: Dict,
        regions: List[str],
        max_actions: int = 3
    ) -> List[Tuple[ActionType, Optional[str], float]]:
        context = self.build_status_prompt(campaign, world_state)

        prompt = f"""{context}

        DECISION TASK:
        Based on the campaign status and polling above, recommend up to {max_actions} campaign actions for this week.

        For each recommended action, provide:
        1. Action type (from available actions list)
        2. Region (or "NATIONAL" for national campaigns)
        3. Intensity (0.0-1.0, where higher intensity = higher cost and effect)
        4. Issue (optional, e.g. "economy" or "healthcare") -- only relevant
           for ISSUE_AD and POLICY_SPEECH, where it targets voters who care
           about that specific issue.

        Consider:
        - Where are you strongest/weakest compared to opponents?
        - Which regions have the most persuadable voters?
        - Which issues does the electorate care about most right now?
        - What's the ROI on each action type?
        - How much budget do you have left?

        Format your response as JSON with this structure:
        {{
            "reasoning": "Brief explanation of strategy",
            "recommended_actions": [
                {{
                    "action": "MEDIA_CAMPAIGN",
                    "region": "North",
                    "intensity": 0.7,
                    "issue": null
                }}
            ]
        }}

        Respond with ONLY the JSON, no other text."""

        try:
            response = self._request_model_output(prompt).strip()
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                decision_data = json.loads(json_str)

                actions = []
                for action_rec in decision_data.get("recommended_actions", []):
                    try:
                        action_type = ActionType[action_rec.get("action", "").upper()]
                        region = action_rec.get("region", "").upper()
                        region = None if region == "NATIONAL" else region
                        intensity = float(action_rec.get("intensity", 0.5))
                        intensity = max(0.0, min(1.0, intensity))
                        issue = action_rec.get("issue") or None
                        actions.append((action_type, region, intensity, issue))
                    except (KeyError, ValueError):
                        continue

                return actions[:max_actions]

            return self.default_plan(campaign, world_state, regions)

        except Exception:
            return self.default_plan(campaign, world_state, regions)

    def default_plan(
        self,
        campaign: CampaignState,
        world_state: Dict,
        regions: List[str]
    ) -> List[Tuple[ActionType, Optional[str], float]]:
        if campaign.cash_on_hand < 10000:
            return [(ActionType.FUNDRAISING, None, 0.8)]

        actions = []

        if campaign.cash_on_hand < 80000:
            actions.append((ActionType.FUNDRAISING, None, 0.7))

        regional_affinity = world_state.get('regional_affinity', {})
        if regional_affinity:
            support_by_region = {}
            for region_name, affinity_dict in regional_affinity.items():
                support_by_region[region_name] = affinity_dict.get(self.candidate_name, 0.5)

            if support_by_region:
                weakest_region = min(support_by_region.items(), key=lambda x: x[1])[0]
                actions.append((ActionType.DOOR_TO_DOOR, weakest_region, 0.6))
                actions.append((ActionType.PHONE_BANK, weakest_region, 0.5))

        if campaign.cash_on_hand > 50000:
            actions.append((ActionType.MEDIA_CAMPAIGN, None, 0.5))
            actions.append((ActionType.ISSUE_AD, None, 0.5, top_issue(world_state)))

        if campaign.cash_on_hand > 15000:
            actions.append((ActionType.SOCIAL_MEDIA, None, 0.4))
            actions.append((ActionType.MICRO_TARGETING, None, 0.4))

        return actions[:3]


class StrategyAgent:
    def __init__(self, strategy: str = "balanced"):
        self.strategy = strategy
        self.candidate_name = None

    def set_candidate(self, candidate_name: str):
        self.candidate_name = candidate_name

    def decide_actions(
        self,
        campaign: CampaignState,
        world_state: Dict,
        regions: List[str],
        max_actions: int = 3
    ) -> List[Tuple[ActionType, Optional[str], float]]:
        if self.strategy == "balanced":
            return self.balanced(campaign, world_state, regions, max_actions)
        if self.strategy == "grassroots":
            return self.grassroots(campaign, regions, max_actions)
        if self.strategy == "media_blitz":
            return self.media_blitz(campaign, world_state, regions, max_actions)
        if self.strategy == "targeted":
            return self.targeted(campaign, world_state, regions, max_actions)
        return self.balanced(campaign, world_state, regions, max_actions)

    def balanced(self, campaign: CampaignState, world_state: Dict, regions: List[str], max_actions: int) -> List:
        actions = []
        if campaign.cash_on_hand < 80000:
            actions.append((ActionType.FUNDRAISING, None, 0.7))
        if campaign.cash_on_hand > 60000:
            actions.append((ActionType.MEDIA_CAMPAIGN, None, 0.6))
        if campaign.cash_on_hand > 25000 and len(regions) > 0:
            actions.append((ActionType.PHONE_BANK, regions[0], 0.5))
        if campaign.cash_on_hand > 15000 and len(regions) > 0:
            actions.append((ActionType.RALLY, regions[0], 0.5))
        if campaign.cash_on_hand > 10000:
            actions.append((ActionType.SOCIAL_MEDIA, None, 0.4))
        if campaign.cash_on_hand > 20000:
            actions.append((ActionType.ISSUE_AD, None, 0.5, top_issue(world_state)))
        return actions[:max_actions]

    def grassroots(self, campaign: CampaignState, regions: List[str], max_actions: int) -> List:
        actions = []
        if campaign.cash_on_hand < 75000:
            actions.append((ActionType.FUNDRAISING, None, 0.8))
        if campaign.cash_on_hand > 10000 and len(regions) > 0:
            actions.append((ActionType.DOOR_TO_DOOR, regions[0], 0.7))
        if campaign.cash_on_hand > 10000 and len(regions) > 1:
            actions.append((ActionType.VOTER_REGISTRATION, regions[1], 0.6))
        if campaign.cash_on_hand > 10000:
            actions.append((ActionType.TOWN_HALL, None, 0.5))
        if campaign.cash_on_hand > 15000:
            actions.append((ActionType.PHONE_BANK, regions[0], 0.5))
        return actions[:max_actions]

    def media_blitz(self, campaign: CampaignState, world_state: Dict, regions: List[str], max_actions: int) -> List:
        actions = []
        if campaign.cash_on_hand < 90000:
            actions.append((ActionType.FUNDRAISING, None, 0.7))
        if campaign.cash_on_hand > 80000:
            actions.append((ActionType.MEDIA_CAMPAIGN, None, 0.8))
        if campaign.cash_on_hand > 40000:
            actions.append((ActionType.ISSUE_AD, None, 0.6, top_issue(world_state)))
        if campaign.cash_on_hand > 20000:
            actions.append((ActionType.SOCIAL_MEDIA, None, 0.7))
        if campaign.cash_on_hand > 15000:
            actions.append((ActionType.MICRO_TARGETING, None, 0.5))
        return actions[:max_actions]

    def targeted(self, campaign: CampaignState, world_state: Dict, regions: List[str], max_actions: int) -> List:
        actions = []
        if campaign.cash_on_hand < 75000:
            actions.append((ActionType.FUNDRAISING, None, 0.8))

        regional_affinity = world_state.get('regional_affinity', {})

        if regional_affinity:
            support_by_region = {}
            for region_name, affinity_dict in regional_affinity.items():
                support_by_region[region_name] = affinity_dict.get(self.candidate_name, 0.5)

            sorted_regions = sorted(support_by_region.items(), key=lambda x: x[1])

            if campaign.cash_on_hand > 10000:
                actions.append((ActionType.DOOR_TO_DOOR, sorted_regions[0][0], 0.7))
            if campaign.cash_on_hand > 15000 and len(sorted_regions) > 1:
                actions.append((ActionType.PHONE_BANK, sorted_regions[0][0], 0.5))
            if campaign.cash_on_hand > 20000 and len(sorted_regions) > 1:
                actions.append((ActionType.MICRO_TARGETING, sorted_regions[1][0], 0.5))

        if campaign.cash_on_hand > 50000:
            actions.append((ActionType.ISSUE_AD, None, 0.5, top_issue(world_state)))

        return actions[:max_actions]

