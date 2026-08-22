from typing import Dict, List, Tuple, Optional
import numpy as np
from simulation.campaignaction import CampaignAction, ActionType, ActionEffects
from simulation.voters import Voter


class CampaignEffects:

    @staticmethod
    def get_fundraising_revenue(action: CampaignAction) -> float:
        return ActionEffects.get_fundraising_revenue(action)

    @staticmethod
    def get_popularity_impact(action: CampaignAction) -> float:
        return ActionEffects.get_popularity_impact(action)
    
    @staticmethod
    def apply_action_to_voter(voter: Voter,
                            candidate_name: str,
                            action: CampaignAction,
                            candidate_affinity: float) -> Tuple[float, float]:
        voter_impact = ActionEffects.get_voter_impact(action, voter.engagement)

        if action.action_type == ActionType.OPPOSITION_RESEARCH:
            knowledge_resistance = max(0.0, 1.0 - voter.political_knowledge)
            voter_impact *= (0.55 + 0.45 * (1.0 - knowledge_resistance))

        turnout_change = ActionEffects.get_turnout_impact(action)

        if action.region and hasattr(voter, 'region'):
            if action.region.lower() == voter.region.lower():
                voter_impact *= 1.5
            else:
                voter_impact *= 0.45

        if action.action_type in {ActionType.MICRO_TARGETING, ActionType.PHONE_BANK}:
            voter_impact *= (0.8 + candidate_affinity * 0.8)

        if voter_impact > 0:
            persuasion_gap = max(0.10, 1.0 - candidate_affinity)
            voter_impact *= persuasion_gap
        else:
            hostility_gap = max(0.10, candidate_affinity)
            voter_impact *= hostility_gap

        voter_impact = float(np.clip(voter_impact, -0.06, 0.06))
        turnout_change = float(np.clip(turnout_change, -0.08, 0.12))

        return voter_impact, turnout_change
    
    @staticmethod
    def apply_action_to_region(action: CampaignAction,
                              region_voters: List[Voter],
                              candidate_name: str,
                              candidate_affinity_dict: Dict[str, float]) -> Tuple[float, int]:
        if not region_voters:
            return 0.0, 0
        
        total_affinity_change = 0.0
        voters_affected = 0
        
        reach_multiplier = ActionEffects.REACH.get(action.action_type, 1.0)
        base_reach = 0.18 + 0.22 * reach_multiplier * action.intensity
        reach_proportion = min(1.0, base_reach)

        num_voters_reached = max(1, int(len(region_voters) * reach_proportion))

        if action.action_type == ActionType.DOOR_TO_DOOR:
            targeted_voters = np.random.choice(region_voters, size=num_voters_reached, replace=False)
        elif action.action_type in [ActionType.MEDIA_CAMPAIGN, ActionType.ISSUE_AD, ActionType.SOCIAL_MEDIA]:
            sorted_voters = sorted(region_voters, key=lambda v: v.engagement, reverse=True)
            targeted_voters = sorted_voters[:num_voters_reached]
        elif action.action_type in [ActionType.RALLY, ActionType.TOWN_HALL, ActionType.SURROGATE_VISIT]:
            sorted_voters = sorted(region_voters, key=lambda v: v.political_interest, reverse=True)
            targeted_voters = sorted_voters[:num_voters_reached]
        elif action.action_type in [ActionType.VOTER_REGISTRATION, ActionType.PHONE_BANK]:
            sorted_voters = sorted(region_voters, key=lambda v: (v.turnout_probability, v.engagement), reverse=True)
            targeted_voters = sorted_voters[:num_voters_reached]
        elif action.action_type == ActionType.MICRO_TARGETING:
            sorted_voters = sorted(region_voters, key=lambda v: (v.engagement, v.political_interest), reverse=True)
            targeted_voters = sorted_voters[:num_voters_reached]
        else:
            targeted_voters = np.random.choice(region_voters, size=num_voters_reached, replace=False)
        
        for voter in targeted_voters:
            affinity = candidate_affinity_dict.get(voter.name, 0.5)
            affinity_change, turnout_change = CampaignEffects.apply_action_to_voter(
                voter, candidate_name, action, affinity
            )
            total_affinity_change += affinity_change
            CampaignEffects.update_voter_turnout(voter, turnout_change)
            voters_affected += 1

        avg_change = total_affinity_change / voters_affected if voters_affected > 0 else 0.0
        return avg_change, voters_affected
    
    @staticmethod
    def update_voter_affinity(voter: Voter,
                             candidate_name: str,
                             affinity_change: float) -> float:
        current_affinity = voter.candidate_affinity.get(candidate_name, 0.5)
        new_affinity = np.clip(current_affinity + affinity_change, 0.0, 1.0)
        voter.candidate_affinity[candidate_name] = new_affinity
        return new_affinity

    @staticmethod
    def update_voter_turnout(voter: Voter, turnout_change: float):
        voter.turnout_probability = float(np.clip(voter.turnout_probability + turnout_change, 0.0, 1.0))
        return voter.turnout_probability

    @staticmethod
    def apply_national_action(action: CampaignAction,
                             regions: List,
                             candidate_name: str,
                             candidate_affinity_dict_by_region: Dict[str, Dict[str, float]]) -> Dict:
        results = {}
        
        for region in regions:
            affinity_dict = candidate_affinity_dict_by_region.get(region.name, {})
            avg_change, voters_reached = CampaignEffects.apply_action_to_region(
                action, region.voter_list, candidate_name, affinity_dict
            )
            results[region.name] = {
                "avg_affinity_change": avg_change,
                "voters_reached": voters_reached,
                "total_voters": len(region.voter_list)
            }
        
        return results
    
    @staticmethod
    def calculate_regional_affinity(region, candidate_name: str) -> float:
        if not region.voter_list:
            return 0.5
        
        total_affinity = sum(
            voter.candidate_affinity.get(candidate_name, 0.5)
            for voter in region.voter_list
        )
        return total_affinity / len(region.voter_list)
    
    @staticmethod
    def estimate_vote_share(region, candidate_name: str) -> float:
        total_votes = 0.0
        candidate_votes = 0.0
        
        for voter in region.voter_list:
            turnout_weight = voter.turnout_probability
            affinity = voter.candidate_affinity.get(candidate_name, 0.5)

            momentum = 0.5 + (affinity - 0.5) * 1.2
            intensity_bonus = 0.08 * max(0.0, voter.engagement - 0.4)
            vote_probability = np.clip(momentum + intensity_bonus, 0.02, 0.98)

            total_votes += turnout_weight
            candidate_votes += turnout_weight * vote_probability
        
        if total_votes == 0:
            return 0.5
        
        return candidate_votes / total_votes
    
    @staticmethod
    def get_action_results_summary(action: CampaignAction,
                                   results: Dict[str, Dict]) -> str:
        total_reached = sum(r.get("voters_reached", 0) for r in results.values())
        avg_change = np.mean([r.get("avg_affinity_change", 0) for r in results.values()])
        
        change_str = f"+{avg_change:.1%}" if avg_change >= 0 else f"{avg_change:.1%}"
        
        summary = f"{action.description}: {total_reached:,} voters reached, avg affinity change {change_str}"
        return summary
