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

    def calculate_score(self, voter, party):
        
        policy_match = (((1-(abs(voter.preferences.economy-party.candidate.preferences.economy)/2)))*voter.weights.economy)+((1-(abs(voter.preferences.tax-party.candidate.preferences.tax)/2))*voter.weights.tax)+((1-(abs(voter.preferences.healthcare-party.candidate.preferences.healthcare)/2))*voter.weights.healthcare)+((1-(abs(voter.preferences.education-party.candidate.preferences.education)/2))*voter.weights.education)+((1-(abs(voter.preferences.immigration-party.candidate.preferences.immigration)/2))*voter.weights.immigration+(
        (1-(abs(voter.preferences.environment-party.candidate.preferences.environment)/2))*voter.weights.environment+(1-(abs(voter.preferences.crime-party.candidate.preferences.crime)/2))*voter.weights.crime)+(1-(abs(voter.preferences.government_size-party.candidate.preferences.government_size)/2))*voter.weights.government_size)+((1-(abs(voter.preferences.foreign_policy-party.candidate.preferences.foreign_policy)/2))*voter.weights.foreign_policy)+((1-(abs(voter.preferences.infrastructure-party.candidate.preferences.infrastructure)/2))*voter.weights.infrastructure)/10

        candidate_appeal = (party.candidate.traits.charisma+party.candidate.traits.debate_skill+party.candidate.traits.media_skill+party.candidate.traits.fundraising+party.candidate.traits.organization+party.candidate.traits.discipline+party.candidate.traits.persuasion+party.candidate.traits.leadership+party.candidate.traits.authenticity+party.candidate.traits.experience+party.candidate.traits.risk_tolerance+party.candidate.traits.coalition_building)/10

        party_preference = (voter.party_affinity[party.name]+1)/2

        random_variation = np.random.uniform(0,1)

        score = (0.7*policy_match+0.1*candidate_appeal+0.1*party_preference+0.1*random_variation)*1/party.popularity
        
        return score

    def ask_voters(self, voter, parties):
        scores = {}

        for party in parties:
            scores[party.candidate.name] = 1/self.calculate_score(voter, party)

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

    
