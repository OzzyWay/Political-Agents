import numpy as np
from settings import DEFAULT_CANDIDATES

class Poll: 

    def __init__(self, pollster, sample_size, poll_region):
        self.pollster = pollster
        self.sample_size = sample_size
        self.poll_region = poll_region
        self.sample = np.random.choice(
            poll_region.voter_list,
            size=sample_size,
            replace=False
        )

    def ask_voters(self, voter, parties):
        scores = {}

        for party in parties:
            scores[party.candidate.name] = 1/voter.calculate_score(party)

        score_total = sum(scores.values())

        percent = []
        for party in parties:
            percent.append(
                scores[party.candidate.name] / score_total
            )

        candidates = [f"{party.candidate.name} - {party.name}" for party in parties]

        candidate = np.random.choice(
            candidates,
            p=percent
        )

        return candidate

    def run_poll(self, parties):

        results={}
        for party in parties:
            results[f"{party.candidate.name} - {party.name}"] = 0

        for voter in self.sample:
            response = self.ask_voters(voter, parties)
            results[response]+=1

        self.results = results

    
def runNationalPoll(pollster, sample, regions):
    voters = []
    for region in regions:
        voters.append(region.voter_list)
    
    poll = Poll(pollster, sample, voters)

    poll.run_poll

    return poll