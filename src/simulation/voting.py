import numpy as np


def calculate_vote(voter, parties):
    scores = {}


    for party in parties:
        scores[f"{party.candidate.name} - {party.name}"] = 1/voter.calculate_score(party)
    
    score_total = sum(scores.values())
    percent = []
    for party in parties:
        percent.append(scores[f"{party.candidate.name} - {party.name}"] / score_total)

    candidates = [f"{party.candidate.name} - {party.name}" for party in parties]

    candidate = np.random.choice(
        candidates,
        p=percent
    )

    return candidate

def run_election(regions, parties):

    results={}
    for party in parties:
        results[f"{party.candidate.name} - {party.name}"] = 0

    for region in regions:
        for voter in region.voter_list:
            if voter.turnout_probability >= np.random.uniform(0,1):
                
                results[calculate_vote(voter, parties)] += 1

    return results