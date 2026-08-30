from typing import Dict, List

import numpy as np

from simulation.mathutils import stable_softmax
from simulation.scoring import calculate_vote_score

DEFAULT_TEMPERATURE = 0.12


def calculate_vote_probabilities(voter, parties, temperature: float = DEFAULT_TEMPERATURE) -> Dict[str, float]:
    scores = {
        f"{party.candidate.name} - {party.name}": calculate_vote_score(voter, party)
        for party in parties
    }
    return stable_softmax(scores, temperature=temperature)


def calculate_vote(voter, parties, temperature: float = DEFAULT_TEMPERATURE) -> str:
    probabilities = calculate_vote_probabilities(voter, parties, temperature=temperature)
    labels = list(probabilities.keys())
    weights = list(probabilities.values())
    return str(np.random.choice(labels, p=weights))


def run_election(regions, parties, temperature: float = DEFAULT_TEMPERATURE) -> Dict[str, float]:
    raw_counts: Dict[str, int] = {f"{party.candidate.name} - {party.name}": 0 for party in parties}
    total_votes = 0

    for region in regions:
        for voter in region.voter_list:
            if voter.turnout_probability >= np.random.uniform(0, 1):
                raw_counts[calculate_vote(voter, parties, temperature=temperature)] += 1
                total_votes += 1

    if total_votes == 0:
        even_share = 1.0 / len(parties) if parties else 0.0
        return {label: even_share for label in raw_counts}

    return {label: count / total_votes for label, count in raw_counts.items()}
