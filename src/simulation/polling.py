"""Regional and national polling.

Fixes applied here (Section 12):
  - runNationalPoll no longer builds a list-of-lists of voters; it flattens
    every region's voter_list into one flat sample pool.
  - poll.run_poll(...) is actually *called* (the old code referenced the
    bound method without invoking it, so results were never populated).
"""
from typing import List, Optional

import numpy as np

from simulation.voting import calculate_vote_probabilities


class Poll:

    def __init__(self, pollster, sample_size, voter_pool: List, temperature: float = 0.12):
        self.pollster = pollster
        self.sample_size = min(int(sample_size), len(voter_pool)) if voter_pool else 0
        self.voter_pool = voter_pool
        self.temperature = temperature
        self.results = {}

        if self.sample_size > 0:
            self.sample = np.random.choice(voter_pool, size=self.sample_size, replace=False)
        else:
            self.sample = np.array([])

    def ask_voters(self, voter, parties) -> str:
        probabilities = calculate_vote_probabilities(voter, parties, temperature=self.temperature)
        labels = list(probabilities.keys())
        weights = list(probabilities.values())
        return str(np.random.choice(labels, p=weights))

    def run_poll(self, parties) -> dict:
        results = {f"{party.candidate.name} - {party.name}": 0 for party in parties}

        for voter in self.sample:
            response = self.ask_voters(voter, parties)
            results[response] += 1

        self.results = results
        return results


def run_poll_on_region(pollster: str, sample_size: int, region) -> Poll:
    poll = Poll(pollster, sample_size, region.voter_list)
    return poll


def runNationalPoll(pollster: str, sample_size: int, regions, parties, temperature: float = 0.12) -> Poll:
    voters = []
    for region in regions:
        voters.extend(region.voter_list)

    poll = Poll(pollster, sample_size, voters, temperature=temperature)
    poll.run_poll(parties)

    return poll
