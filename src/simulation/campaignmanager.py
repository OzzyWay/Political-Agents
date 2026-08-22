from typing import Dict, List, Optional, Union
import numpy as np

from simulation.world import World
from simulation.campaignstate import MultiCampaignTracker, WeeklyMetrics
from simulation.campaignaction import CampaignAction, ActionType, ActionEffects
from simulation.campaigneffects import CampaignEffects as VoteEffects
from simulation.aiagent import CampaignAdvisor, StrategyAgent


class CampaignManager:
    def __init__(
        self,
        world: World,
        campaign_weeks: int,
        starting_budget_per_candidate: float = 500000,
        use_ai: bool = False,
        ai_model: str = "llama2",
        ai_strategies: Optional[Dict[str, str]] = None,
    ):
        self.world = world
        self.campaign_weeks = campaign_weeks
        self.starting_budget = starting_budget_per_candidate
        self.use_ai = use_ai

        self.tracker = MultiCampaignTracker(campaign_weeks)
        self.agents: Dict[str, Union[CampaignAdvisor, StrategyAgent]] = {}
        self.affinity_history: Dict[str, List[float]] = {}

        for party in world.parties:
            candidate = party.candidate
            self.tracker.add_candidate(candidate.name, starting_budget_per_candidate)
            self.affinity_history[candidate.name] = []

            if use_ai:
                agent = CampaignAdvisor(model=ai_model)
            else:
                strategy = ai_strategies.get(candidate.name, "balanced") if ai_strategies else "balanced"
                agent = StrategyAgent(strategy=strategy)

            agent.set_candidate(candidate.name)
            self.agents[candidate.name] = agent

    def get_world_state_snapshot(self) -> Dict:
        state = {
            "week": self.tracker.current_week,
            "regional_affinity": {},
            "national_affinity": {},
            "candidate_details": {}
        }

        for region in self.world.regions:
            state["regional_affinity"][region.name] = {}
            for party in self.world.parties:
                candidate = party.candidate
                affinity = VoteEffects.calculate_regional_affinity(region, candidate.name)
                state["regional_affinity"][region.name][candidate.name] = affinity

        for party in self.world.parties:
            candidate = party.candidate
            affinities = [
                VoteEffects.calculate_regional_affinity(region, candidate.name)
                for region in self.world.regions
            ]
            state["national_affinity"][candidate.name] = np.mean(affinities)

        for party in self.world.parties:
            candidate = party.candidate
            campaign = self.tracker.get_candidate_campaign(candidate.name)
            state["candidate_details"][candidate.name] = {
                "cash_on_hand": campaign.cash_on_hand,
                "total_budget": campaign.starting_budget,
                "actions_taken": len(campaign.actions_history),
            }

        return state

    def run_campaign(self) -> Dict:
        print(f"\n{'='*80}")
        print(f"CAMPAIGN SIMULATION: {self.campaign_weeks} weeks")
        print(f"Candidates: {[p.candidate.name for p in self.world.parties]}")
        print(f"{'='*80}\n")

        for week in range(1, self.campaign_weeks + 1):
            print(f"\nWEEK {week}/{self.campaign_weeks}")
            print("-" * 80)

            self._run_week(week)
            self.tracker.advance_week()

        return self._generate_final_report()

    def _run_week(self, week: int):
        world_state = self.get_world_state_snapshot()

        decisions = {}
        for party in self.world.parties:
            candidate = party.candidate
            campaign = self.tracker.get_candidate_campaign(candidate.name)
            agent = self.agents[candidate.name]

            region_names = [r.name for r in self.world.regions]
            action_decisions = agent.decide_actions(
                campaign,
                world_state,
                region_names,
                max_actions=3,
            )
            if not action_decisions:
                action_decisions = [(ActionType.FUNDRAISING, None, 0.5)] if campaign.cash_on_hand < 80000 else [(ActionType.MEDIA_CAMPAIGN, None, 0.5)]
            decisions[candidate.name] = action_decisions

        action_results = {}
        for candidate_name, action_decisions in decisions.items():
            campaign = self.tracker.get_candidate_campaign(candidate_name)
            candidate_results = []

            for action_type, region, intensity in action_decisions:
                action = CampaignAction(
                    action_type=action_type,
                    week=week,
                    region=region,
                    intensity=intensity,
                )

                if campaign.record_action(action):
                    effects = self._apply_action(action, candidate_name)
                    candidate_results.append({
                        "action": action.description,
                        "cost": action.cost,
                        "effects": effects,
                    })
                    print(f"  {candidate_name}: {action.description} (${action.cost:,.0f})")
                else:
                    print(f"  {candidate_name}: Cannot afford {action.description}")

            action_results[candidate_name] = candidate_results

        for party in self.world.parties:
            candidate = party.candidate
            campaign = self.tracker.get_candidate_campaign(candidate.name)

            regional_affinities = []
            total_voters_reached = 0
            total_vote_share = 0.0

            for region in self.world.regions:
                affinity = VoteEffects.calculate_regional_affinity(region, candidate.name)
                regional_affinities.append(affinity)

                vote_share = VoteEffects.estimate_vote_share(region, candidate.name)
                total_vote_share += vote_share

                total_voters_reached += len(region.voter_list)

            avg_affinity = np.mean(regional_affinities) if regional_affinities else 0.5
            avg_vote_share = total_vote_share / len(self.world.regions) if self.world.regions else 0.5

            metrics = WeeklyMetrics(
                week=week,
                candidate_name=candidate.name,
                total_spending=campaign.get_total_spending_this_week(),
                actions_taken=campaign.get_actions_this_week(),
                avg_regional_affinity=avg_affinity,
                voters_reached=total_voters_reached,
                estimated_vote_share=avg_vote_share,
            )
            campaign.record_weekly_metrics(metrics)

            summary = metrics.to_dict()
            print(f"\n  {candidate.name} Summary:")
            print(f"    Avg Affinity: {summary['avg_affinity']:.1%}")
            print(f"    Est. Vote Share: {summary['vote_share']}%")
            print(f"    Cash Remaining: ${summary['cash']:,.0f}")

    def _apply_action(self, action: CampaignAction, candidate_name: str) -> Dict:
        results = {}

        affinity_by_region = {}
        for region in self.world.regions:
            affinity_by_region[region.name] = {
                voter.name: voter.candidate_affinity.get(candidate_name, 0.5)
                for voter in region.voter_list
            }

        if action.action_type == ActionType.FUNDRAISING:
            campaign = self.tracker.get_candidate_campaign(candidate_name)
            raised = ActionEffects.get_fundraising_revenue(action)
            campaign.cash_on_hand += raised
            party = next((party for party in self.world.parties if party.candidate.name == candidate_name), None)
            if party:
                popularity_delta = ActionEffects.get_popularity_impact(action)
                party.adjust_popularity(popularity_delta)
                results["fundraising"] = {
                    "raised": raised,
                    "net_cash_change": raised - action.cost,
                    "cash_after": campaign.cash_on_hand,
                    "popularity_delta": popularity_delta,
                    "popularity_after": party.popularity,
                }
            else:
                results["fundraising"] = {
                    "raised": raised,
                    "net_cash_change": raised - action.cost,
                    "cash_after": campaign.cash_on_hand,
                }
            return results

        popularity_delta = ActionEffects.get_popularity_impact(action)
        party = next((party for party in self.world.parties if party.candidate.name == candidate_name), None)
        if party:
            party.adjust_popularity(popularity_delta)
            results["popularity_delta"] = popularity_delta
            results["popularity_after"] = party.popularity

        if action.region:
            target_region = next((r for r in self.world.regions if r.name == action.region), None)
            if target_region:
                avg_change, voters_reached = VoteEffects.apply_action_to_region(
                    action,
                    target_region.voter_list,
                    candidate_name,
                    affinity_by_region[target_region.name],
                )

                for voter in target_region.voter_list:
                    change = avg_change * (0.5 + 0.5 * np.random.random())
                    VoteEffects.update_voter_affinity(voter, candidate_name, change)

                results[action.region] = {
                    "avg_affinity_change": avg_change,
                    "voters_reached": voters_reached,
                }
        else:
            national_results = VoteEffects.apply_national_action(
                action,
                self.world.regions,
                candidate_name,
                affinity_by_region,
            )

            for region in self.world.regions:
                region_result = national_results.get(region.name, {})
                avg_change = region_result.get("avg_affinity_change", 0.0)

                for voter in region.voter_list:
                    change = avg_change * (0.5 + 0.5 * np.random.random())
                    VoteEffects.update_voter_affinity(voter, candidate_name, change)

            results = national_results

        return results

    def _generate_final_report(self) -> Dict:
        print(f"\n{'='*80}")
        print("CAMPAIGN RESULTS")
        print(f"{'='*80}\n")

        final_state = self.get_world_state_snapshot()
        summaries = self.tracker.get_all_summaries()

        candidates_ranked = []
        for candidate_name, summary in summaries.items():
            print(f"\n{candidate_name}")
            print("-" * 40)
            print(f"Budget Spent: ${summary['total_spent']:,.0f} / ${summary['total_budget']:,.0f}")
            print(f"Cash Remaining: ${summary['cash_remaining']:,.0f}")
            print(f"Total Actions: {summary['total_actions']}")
            print(f"Actions by Type: {summary['actions_by_type']}")

            print(f"\nRegional Support:")
            for region_name, affinity in final_state['regional_affinity'].items():
                candidate_affinity = affinity.get(candidate_name, 0.0)
                print(f"  {region_name}: {candidate_affinity:.1%}")

            print(f"\nNational Average: {final_state['national_affinity'].get(candidate_name, 0.0):.1%}")
            print(f"Est. Vote Share: {summary['final_vote_share']:.1%}")

            candidates_ranked.append((candidate_name, final_state['national_affinity'].get(candidate_name, 0.0)))

        print(f"\n{'='*80}")
        print("FINAL RANKING")
        print(f"{'='*80}\n")

        candidates_ranked.sort(key=lambda x: x[1], reverse=True)
        for rank, (candidate_name, affinity) in enumerate(candidates_ranked, 1):
            print(f"{rank}. {candidate_name}: {affinity:.1%} affinity")

        return {
            "final_state": final_state,
            "campaign_summaries": summaries,
            "rankings": candidates_ranked,
        }
