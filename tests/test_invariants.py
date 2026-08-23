import math
import sys
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from settings import set_global_seed
from simulation.world import World
from simulation.scoring import (
    calculate_issue_match,
    calculate_policy_match,
    calculate_vote_score,
)
from simulation.voting import calculate_vote_probabilities, run_election
from simulation.polling import runNationalPoll
from simulation.campaignaction import CampaignAction, ActionType
from simulation.campaigneffects import CampaignEffects
from simulation.mathutils import stable_softmax, diminishing_return, weighted_average
from simulation.campaignmanager import CampaignManager


SMALL_REGIONS = ["North", "South"]
SMALL_VOTERS = 40


def make_world(regions=SMALL_REGIONS, voters_per_region=SMALL_VOTERS):
    set_global_seed(7)
    return World(regions=regions, voters_per_region=voters_per_region)


def test_issue_match_range():
    assert calculate_issue_match(-1.0, 1.0) == pytest.approx(0.0)
    assert calculate_issue_match(1.0, 1.0) == pytest.approx(1.0)
    for _ in range(200):
        a, b = np.random.uniform(-1, 1, 2)
        match = calculate_issue_match(a, b)
        assert 0.0 <= match <= 1.0


def test_policy_match_range():
    world = make_world()
    voter = world.regions[0].voter_list[0]
    for party in world.parties:
        match = calculate_policy_match(voter.preferences, voter.weights, party.candidate.preferences)
        assert 0.0 <= match <= 1.0


def test_candidate_score_range():
    world = make_world()
    for region in world.regions:
        for voter in region.voter_list[:10]:
            for party in world.parties:
                score = calculate_vote_score(voter, party)
                assert 0.0 <= score <= 1.0
                assert not math.isnan(score)


def test_softmax_probabilities_sum_to_one():
    scores = {"a": 0.9, "b": 0.5, "c": 0.1}
    probs = stable_softmax(scores, temperature=0.2)
    assert sum(probs.values()) == pytest.approx(1.0, abs=1e-9)
    for p in probs.values():
        assert 0.0 <= p <= 1.0


def test_softmax_handles_extreme_scores_without_overflow():
    scores = {"a": 1e6, "b": -1e6, "c": 0.0}
    probs = stable_softmax(scores, temperature=0.01)
    assert all(np.isfinite(p) for p in probs.values())
    assert sum(probs.values()) == pytest.approx(1.0, abs=1e-6)


def test_vote_probabilities_valid():
    world = make_world()
    voter = world.regions[0].voter_list[0]
    probs = calculate_vote_probabilities(voter, world.parties)
    assert sum(probs.values()) == pytest.approx(1.0, abs=1e-6)
    assert all(0.0 <= p <= 1.0 for p in probs.values())


def test_turnout_range():
    world = make_world()
    for region in world.regions:
        for voter in region.voter_list:
            assert 0.0 <= voter.turnout_probability <= 1.0


def test_vote_share_sum():
    world = make_world()
    shares = run_election(world.regions, world.parties)
    assert sum(shares.values()) == pytest.approx(1.0, abs=1e-6)
    for share in shares.values():
        assert 0.0 <= share <= 1.0


def test_campaign_cannot_overspend():
    world = make_world()
    manager = CampaignManager(world=world, campaign_weeks=1, starting_budget_per_candidate=1000, use_ai=False)
    candidate_name = world.parties[0].candidate.name
    campaign = manager.tracker.get_candidate_campaign(candidate_name)

    expensive_action = CampaignAction(action_type=ActionType.MEDIA_CAMPAIGN, week=1, intensity=1.0)
    assert expensive_action.cost > 1000
    assert campaign.record_action(expensive_action) is False
    assert campaign.cash_on_hand == 1000


def test_campaign_effect_is_clamped():
    world = make_world()
    voter = world.regions[0].voter_list[0]
    candidate = world.parties[0].candidate
    action = CampaignAction(action_type=ActionType.RALLY, week=1, intensity=1.0)
    affinity_change, turnout_change = CampaignEffects.apply_action_to_voter(
        voter, candidate, action, candidate_affinity=1.0, week=1
    )
    assert -0.06 <= affinity_change <= 0.06
    assert -0.08 <= turnout_change <= 0.12


def test_diminishing_returns_decreases_with_use():
    values = [diminishing_return(n, decay_factor=0.35) for n in range(5)]
    assert values[0] == pytest.approx(1.0)
    assert all(values[i] > values[i + 1] for i in range(len(values) - 1))
    assert all(0.0 < v <= 1.0 for v in values)


def test_national_weighting_respects_population():
    # A tiny region should barely move the population-weighted average,
    # while a plain mean would give it equal footing with the big one.
    big_value, small_value = 1.0, 0.0
    weighted = weighted_average([big_value, small_value], [1000, 1])
    assert weighted > 0.99  # dominated by the big region
    plain_mean = (big_value + small_value) / 2
    assert weighted != pytest.approx(plain_mean)


def test_national_poll_samples_flat_voter_list_and_produces_valid_results():
    world = make_world()
    poll = runNationalPoll("Test Pollster", sample_size=25, regions=world.regions, parties=world.parties)

    assert all(hasattr(v, "region") for v in poll.sample)
    assert len(poll.sample) == 25
    assert poll.results  # run_poll must actually have been called
    assert sum(poll.results.values()) == 25
    for count in poll.results.values():
        assert count >= 0


def test_reproducible_seed():
    set_global_seed(123)
    world_a = make_world()
    shares_a = run_election(world_a.regions, world_a.parties)

    set_global_seed(123)
    world_b = make_world()
    shares_b = run_election(world_b.regions, world_b.parties)

    for name in shares_a:
        assert shares_a[name] == pytest.approx(shares_b[name])
