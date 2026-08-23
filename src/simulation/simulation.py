"""Top-level entry point that ties World + CampaignManager together behind
a reproducible seed (Section 20).

    sim = Simulation(regions=["North", "South"], seed=42)
    report = sim.run_campaign(weeks=8)

Running with seed=42 twice produces the same outcome; a different seed
produces a different outcome.
"""
from typing import Dict, List, Optional

from settings import DEFAULT_REGIONS, REGION_VOTERS, set_global_seed
from simulation.world import World
from simulation.campaignmanager import CampaignManager


class Simulation:
    def __init__(
        self,
        regions: Optional[List[str]] = None,
        voters_per_region: int = REGION_VOTERS,
        seed: Optional[int] = None,
        starting_budget_per_candidate: float = 500000,
        use_ai: bool = False,
        ai_model: str = "llama2",
        ai_strategies: Optional[Dict[str, str]] = None,
    ):
        self.seed = seed
        if seed is not None:
            set_global_seed(seed)

        self.regions = regions or list(DEFAULT_REGIONS)
        self.voters_per_region = voters_per_region
        self.world = World(regions=self.regions, voters_per_region=self.voters_per_region)
        self._starting_budget_per_candidate = starting_budget_per_candidate
        self._use_ai = use_ai
        self._ai_model = ai_model
        self._ai_strategies = ai_strategies

    def new_campaign_manager(self, campaign_weeks: int) -> CampaignManager:
        return CampaignManager(
            world=self.world,
            campaign_weeks=campaign_weeks,
            starting_budget_per_candidate=self._starting_budget_per_candidate,
            use_ai=self._use_ai,
            ai_model=self._ai_model,
            ai_strategies=self._ai_strategies,
        )

    def run_campaign(self, weeks: int = 8) -> Dict:
        manager = self.new_campaign_manager(weeks)
        return manager.run_campaign()
