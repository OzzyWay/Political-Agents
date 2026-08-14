import numpy as np

from settings import EDUCATION_LEVELS, EDUCATION_WEIGHTS, REGION_VOTERS, DEFAULT_REGIONAL_LEAN, DEFAULT_PARTIES, DEFAULT_PARTY_PREFERENCES, DEFAULT_CANDIDATES
from simulation.preferencesweights import Preferences, Weights
from simulation.parties import getPartyAffinity

class Voter:

    def __init__(self, id, name, age, region, parties):
        self.id = id
        self.name = name
        self.age = age
        self.income = round(np.random.lognormal(mean=np.log(65000), sigma=0.6))
        self.education = np.random.choice(EDUCATION_LEVELS, p=EDUCATION_WEIGHTS)
        self.region = region

        self.turnout_probability = np.clip(np.random.normal(loc=0.6, scale=0.1), 0, 1)

        region_data = DEFAULT_REGIONAL_LEAN.get(region, {})
        region_preferences = region_data.get("preferences", {})
        region_weights = region_data.get("weights", {})
        region_variation = region_data.get("variation", 0.1)

        self.preferences = Preferences(
            economy=region_preferences.get("economy", 0.5) + np.random.normal(0, region_variation),
            tax=region_preferences.get("taxes", 0.5) + np.random.normal(0, region_variation),
            healthcare=region_preferences.get("healthcare", 0.5) + np.random.normal(0, region_variation),
            education=region_preferences.get("education", 0.5) + np.random.normal(0, region_variation),
            immigration=region_preferences.get("immigration", 0.5) + np.random.normal(0, region_variation),
            environment=region_preferences.get("environment", 0.5) + np.random.normal(0, region_variation),
            crime=region_preferences.get("crime", 0.5) + np.random.normal(0, region_variation),
            government_size=region_preferences.get("government_size", 0.5) + np.random.normal(0, region_variation),
            foreign_policy=region_preferences.get("foreign_policy", 0.5) + np.random.normal(0, region_variation),
            infrastructure=region_preferences.get("infrastructure", 0.5) + np.random.normal(0, region_variation)
        )

        self.weights = Weights(
            economy=region_weights.get("economy", 0.5) + np.random.normal(0, region_variation),
            tax=region_weights.get("taxes", 0.5) + np.random.normal(0, region_variation),
            healthcare=region_weights.get("healthcare", 0.5) + np.random.normal(0, region_variation),
            education=region_weights.get("education", 0.5) + np.random.normal(0, region_variation),
            immigration=region_weights.get("immigration", 0.5) + np.random.normal(0, region_variation),
            environment=region_weights.get("environment", 0.5) + np.random.normal(0, region_variation),
            crime=region_weights.get("crime", 0.5) + np.random.normal(0, region_variation),
            government_size=region_weights.get("government_size", 0.5) + np.random.normal(0, region_variation),
            foreign_policy=region_weights.get("foreign_policy", 0.5) + np.random.normal(0, region_variation),
            infrastructure=region_weights.get("infrastructure", 0.5) + np.random.normal(0, region_variation)
        )


        self.party_affinity = {party.name: getPartyAffinity(self, party) for party in parties}

    def __repr__(self):
        return f"Voter(id={self.id}, \nname='{self.name}', \nage={self.age}, \nincome={self.income}, education='{self.education}', \nregion='{self.region}', \nturnout_probability={self.turnout_probability}, \npreferences={self.preferences},\n weights={self.weights})\n"



def GenerateVoterList(region, num_voters, parties):

    voters = [Voter(id=i, name=f"Voter {i}", age=np.random.randint(18, 80), region=region, parties=parties) for i in range(num_voters)]

    for voter in voters:
        print(voter)
    return voters
