from simulation.aiagent import StrategyAgent
from simulation.campaignstate import CampaignState
from simulation.strategies import PRESETS


def test_strategy_agent_custom_returns_actions():
    params = PRESETS["digital_first"]
    agent = StrategyAgent(strategy="custom", style_params=params)
    campaign = CampaignState("TestCandidate", starting_budget=100000, total_weeks=4)
    world_state = {"regional_affinity": {}, "issues": {}, "national_affinity": {}}
    regions = ["North", "South"]
    actions = agent.decide_actions(campaign, world_state, regions, max_actions=3)
    assert isinstance(actions, list)
    assert len(actions) <= 3
    for a in actions:
        assert isinstance(a, tuple)
        assert len(a) >= 3
