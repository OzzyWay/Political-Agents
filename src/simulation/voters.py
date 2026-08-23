import numpy as np

from settings import EDUCATION_LEVELS, EDUCATION_WEIGHTS, DEFAULT_REGIONAL_LEAN, EDUCATION_SCORE
from simulation.preferencesweights import Preferences, Weights
from simulation.memory import VoterMemory
from simulation import scoring


class Voter:

    def __init__(self, id, name, age, region, parties):
        self.id = id
        self.name = name
        self.age = age
        self.income = round(np.random.lognormal(mean=np.log(65000), sigma=0.6))
        self.education = np.random.choice(EDUCATION_LEVELS, p=EDUCATION_WEIGHTS)
        self.education_score = EDUCATION_SCORE[EDUCATION_LEVELS.index(self.education)]
        self.region = region

        region_data = DEFAULT_REGIONAL_LEAN.get(region, {})
        region_preferences = region_data.get("preferences", {})
        region_weights = region_data.get("weights", {})
        region_variation = region_data.get("variation", 0.1)

        self.preferences = Preferences(
            economy=region_preferences.get("economy", 0.0) + np.random.normal(0, region_variation),
            tax=region_preferences.get("taxes", 0.0) + np.random.normal(0, region_variation),
            healthcare=region_preferences.get("healthcare", 0.0) + np.random.normal(0, region_variation),
            education=region_preferences.get("education", 0.0) + np.random.normal(0, region_variation),
            immigration=region_preferences.get("immigration", 0.0) + np.random.normal(0, region_variation),
            environment=region_preferences.get("environment", 0.0) + np.random.normal(0, region_variation),
            crime=region_preferences.get("crime", 0.0) + np.random.normal(0, region_variation),
            government_size=region_preferences.get("government_size", 0.0) + np.random.normal(0, region_variation),
            foreign_policy=region_preferences.get("foreign_policy", 0.0) + np.random.normal(0, region_variation),
            infrastructure=region_preferences.get("infrastructure", 0.0) + np.random.normal(0, region_variation),
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
            infrastructure=region_weights.get("infrastructure", 0.5) + np.random.normal(0, region_variation),
        )

        self.party_affinity = {party.name: scoring.calculate_party_affinity(self, party) for party in parties}
        self.candidate_affinity = {
            party.candidate.name: scoring.calculate_candidate_affinity(self, party.candidate)
            for party in parties
        }

        self.age_factor = np.clip((self.age - 18) / 60, 0, 1)
        self.income_factor = np.clip(np.log(self.income / 20000) / 4, 0, 1)

        self.political_interest = np.clip(
            0.35 * self.education_score + 0.25 * self.age_factor + 0.20 * self.income_factor
            + 0.20 * np.random.random(),
            0, 1,
        )

        self.issue_importance = np.clip(np.mean(list(self.weights.as_dict().values())), 0, 1)

        self.political_knowledge = np.clip(0.6 * self.education_score + 0.4 * self.political_interest, 0, 1)

        self.social_exposure = np.clip(np.random.normal(0.5, 0.2), 0, 1)

        self.engagement = np.clip(
            0.35 * self.political_interest + 0.30 * self.issue_importance
            + 0.20 * self.political_knowledge + 0.15 * self.social_exposure,
            0, 1,
        )

        self.turnout_probability = float(
            np.clip(1 / (1 + np.exp(-(-1.2 + 2.5 * self.engagement + 0.8 * self.age_factor))), 0, 1)
        )

        self.memory = VoterMemory()
        self.action_exposure_counts = {}

    def calculate_score(self, party) -> float:
        """Overall score this voter assigns `party`'s candidate.

        Higher score always means the voter prefers the candidate more.
        Thin wrapper kept for backward compatibility with callers that
        still call voter.calculate_score(party) directly.
        """
        return scoring.calculate_vote_score(self, party)

    def __repr__(self):
        return (
            f"Voter(id={self.id}, \nname='{self.name}', \nage={self.age}, \nincome={self.income}, "
            f"education='{self.education}', \nregion='{self.region}', "
            f"\nturnout_probability={self.turnout_probability}, \npreferences={self.preferences},\n "
            f"weights={self.weights})\n"
        )


def GenerateVoterList(region, num_voters, parties):
    voters = [
        Voter(id=i, name=f"Voter {i}", age=np.random.randint(18, 80), region=region, parties=parties)
        for i in range(num_voters)
    ]
    return voters
