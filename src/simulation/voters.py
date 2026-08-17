import numpy as np

from settings import EDUCATION_LEVELS, EDUCATION_WEIGHTS, REGION_VOTERS, DEFAULT_REGIONAL_LEAN, DEFAULT_PARTIES, DEFAULT_PARTY_PREFERENCES, DEFAULT_CANDIDATES, EDUCATION_SCORE
from simulation.preferencesweights import Preferences, Weights
from simulation.parties import getPartyAffinity

class Voter:

    def __init__(self, id, name, age, region, parties):
        self.id = id
        self.name = name
        self.age = age
        self.income = round(np.random.lognormal(mean=np.log(65000), sigma=0.6))
        self.education = np.random.choice(EDUCATION_LEVELS, p=EDUCATION_WEIGHTS)
        self.education_score = EDUCATION_SCORE[EDUCATION_LEVELS.index(self.education)]
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
        self.candidate_affinity = {party.candidate.name: party.candidate.calculate_voter_affinity(self) for party in parties}
        self.age_factor = np.clip((self.age - 18) / 60, 0, 1)
        self.income_factor = np.clip(np.log(self.income / 20000) / 4, 0, 1)

        self.political_interest = np.clip(0.35 * self.education_score + 0.25 * self.age_factor + 0.20 * self.income_factor + 0.20 * np.random.random(), 0, 1)

        self.issue_importance = np.clip(np.mean(list(vars(self.weights).values())),0,1)

        self.political_knowledge = np.clip(0.6 * self.education_score + 0.4 * self.political_interest,0,1)

        self.social_exposure = np.clip(np.random.normal(0.5, 0.2),0,1)

        self.engagement = np.clip(0.35 * self.political_interest + 0.30 * self.issue_importance + 0.20 * self.political_knowledge + 0.15 * self.social_exposure,0,1)

        self.turnout_probability = 1 / (1 + np.exp(-(-1.2+ 2.5 * self.engagement+ 0.8 * self.age_factor)))

    def calculate_score(self, party):
        
        policy_match = (((1-(abs(self.preferences.economy-party.candidate.preferences.economy)/2)))*self.weights.economy)+((1-(abs(self.preferences.tax-party.candidate.preferences.tax)/2))*self.weights.tax)+((1-(abs(self.preferences.healthcare-party.candidate.preferences.healthcare)/2))*self.weights.healthcare)+((1-(abs(self.preferences.education-party.candidate.preferences.education)/2))*self.weights.education)+((1-(abs(self.preferences.immigration-party.candidate.preferences.immigration)/2))*self.weights.immigration+(
        (1-(abs(self.preferences.environment-party.candidate.preferences.environment)/2))*self.weights.environment+(1-(abs(self.preferences.crime-party.candidate.preferences.crime)/2))*self.weights.crime)+(1-(abs(self.preferences.government_size-party.candidate.preferences.government_size)/2))*self.weights.government_size)+((1-(abs(self.preferences.foreign_policy-party.candidate.preferences.foreign_policy)/2))*self.weights.foreign_policy)+((1-(abs(self.preferences.infrastructure-party.candidate.preferences.infrastructure)/2))*self.weights.infrastructure)/10

        candidate_appeal = (party.candidate.traits.charisma+party.candidate.traits.debate_skill+party.candidate.traits.media_skill+party.candidate.traits.fundraising+party.candidate.traits.organization+party.candidate.traits.discipline+party.candidate.traits.persuasion+party.candidate.traits.leadership+party.candidate.traits.authenticity+party.candidate.traits.experience+party.candidate.traits.risk_tolerance+party.candidate.traits.coalition_building)/10

        party_preference = (self.party_affinity[party.name]+1)/2

        random_variation = np.random.uniform(0,1)

        score = (0.6*policy_match+0.1*candidate_appeal+0.1*party_preference+0.1*random_variation+0.1*self.engagement)*1/party.popularity
        
        return score

    def __repr__(self):
        return f"Voter(id={self.id}, \nname='{self.name}', \nage={self.age}, \nincome={self.income}, education='{self.education}', \nregion='{self.region}', \nturnout_probability={self.turnout_probability}, \npreferences={self.preferences},\n weights={self.weights})\n"



def GenerateVoterList(region, num_voters, parties):

    voters = [Voter(id=i, name=f"Voter {i}", age=np.random.randint(18, 80), region=region, parties=parties) for i in range(num_voters)]
    return voters
