from __future__ import annotations

from simulation.mathutils import clamp
from simulation.preferencesweights import POLICY_KEYS

POLICY_WEIGHT = 0.55
CANDIDATE_WEIGHT = 0.15
PARTY_WEIGHT = 0.15
ENGAGEMENT_WEIGHT = 0.15

AFFINITY_POLICY_WEIGHT = 0.7
AFFINITY_APPEAL_WEIGHT = 0.3


def calculate_issue_match(voter_position: float, candidate_position: float) -> float:
    """Per-issue agreement, always in [0, 1].

    0.0 = complete disagreement (positions on opposite extremes)
    1.0 = perfect agreement (identical positions)
    """
    voter_position = clamp(float(voter_position), -1.0, 1.0)
    candidate_position = clamp(float(candidate_position), -1.0, 1.0)
    distance = abs(voter_position - candidate_position)
    return clamp(1.0 - distance / 2.0, 0.0, 1.0)


def calculate_policy_match(voter_preferences, voter_weights, other_preferences) -> float:
    weighted_sum = 0.0
    weight_total = 0.0

    for key in POLICY_KEYS:
        voter_position = getattr(voter_preferences, key)
        other_position = getattr(other_preferences, key)
        weight = max(0.0, float(getattr(voter_weights, key)))

        weighted_sum += calculate_issue_match(voter_position, other_position) * weight
        weight_total += weight

    if weight_total <= 0.0:
        return 0.5

    return clamp(weighted_sum / weight_total, 0.0, 1.0)


def calculate_candidate_appeal(candidate) -> float:
    trait_values = list(vars(candidate.traits).values())
    if not trait_values:
        return 0.5
    return clamp(sum(trait_values) / len(trait_values), 0.0, 1.0)


def calculate_party_affinity(voter, party) -> float:
    return calculate_policy_match(voter.preferences, voter.weights, party.preferences)


def calculate_candidate_affinity(voter, candidate) -> float:
    policy_match = calculate_policy_match(voter.preferences, voter.weights, candidate.preferences)
    appeal = calculate_candidate_appeal(candidate)
    affinity = AFFINITY_POLICY_WEIGHT * policy_match + AFFINITY_APPEAL_WEIGHT * appeal
    return clamp(affinity, 0.0, 1.0)


def calculate_vote_score(voter, party) -> float:
    policy_match = calculate_policy_match(voter.preferences, voter.weights, party.candidate.preferences)
    candidate_appeal = calculate_candidate_appeal(party.candidate)
    party_component = clamp(party.popularity, 0.0, 1.0)
    engagement_component = clamp(voter.engagement, 0.0, 1.0)

    score = (
        POLICY_WEIGHT * policy_match
        + CANDIDATE_WEIGHT * candidate_appeal
        + PARTY_WEIGHT * party_component
        + ENGAGEMENT_WEIGHT * engagement_component
    )
    return clamp(score, 0.0, 1.0)
