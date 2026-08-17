from settings import DEFAULT_PARTY_PREFERENCES, DEFAULT_PARTIES, DEFAULT_CANDIDATES
from simulation.preferencesweights import Preferences, Weights
import numpy as np

def getPartyAffinity(target, party):
    score = 0
    score += abs(target.preferences.economy - party.preferences.economy)
    score += abs(target.preferences.tax - party.preferences.tax)
    score += abs(target.preferences.healthcare - party.preferences.healthcare)
    score += abs(target.preferences.education - party.preferences.education)
    score += abs(target.preferences.immigration - party.preferences.immigration)
    score += abs(target.preferences.environment - party.preferences.environment)
    score += abs(target.preferences.crime - party.preferences.crime)
    score += abs(target.preferences.government_size - party.preferences.government_size)
    score += abs(target.preferences.foreign_policy - party.preferences.foreign_policy)
    score += abs(target.preferences.infrastructure - party.preferences.infrastructure)

    score += abs(target.weights.economy - party.weights.economy)
    score += abs(target.weights.tax - party.weights.tax)
    score += abs(target.weights.healthcare - party.weights.healthcare)
    score += abs(target.weights.education - party.weights.education)
    score += abs(target.weights.immigration - party.weights.immigration)
    score += abs(target.weights.environment - party.weights.environment)
    score += abs(target.weights.crime - party.weights.crime)
    score += abs(target.weights.government_size - party.weights.government_size)
    score += abs(target.weights.foreign_policy - party.weights.foreign_policy)
    score += abs(target.weights.infrastructure - party.weights.infrastructure)

    return score

class CandidateTraits:
    def __init__(self, charisma, debate_skill, media_skill, fundraising, organization, discipline, persuasion, leadership, authenticity, experience, risk_tolerance, coalition_building):
        self.charisma = charisma
        self.debate_skill = debate_skill
        self.media_skill = media_skill
        self.fundraising = fundraising
        self.organization = organization
        self.discipline = discipline
        self.persuasion = persuasion
        self.leadership = leadership
        self.authenticity = authenticity
        self.experience = experience
        self.risk_tolerance = risk_tolerance
        self.coalition_building = coalition_building

    def __repr__(self):
        return f"CandidateTraits(charisma={self.charisma}, debate_skill={self.debate_skill}, media_skill={self.media_skill}, fundraising={self.fundraising}, organization={self.organization}, discipline={self.discipline}, persuasion={self.persuasion}, leadership={self.leadership}, authenticity={self.authenticity}, experience={self.experience}, risk_tolerance={self.risk_tolerance}, coalition_building={self.coalition_building})"


class Candidate:
    def __init__(self, party):
        self.name = DEFAULT_CANDIDATES[party]["name"]
        self.party = party
        self.preferences = Preferences(DEFAULT_CANDIDATES[party]["preferences"]["economy"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["taxes"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["healthcare"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["education"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["immigration"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["environment"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["crime"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["government_size"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["foreign_policy"],
                                       DEFAULT_CANDIDATES[party]["preferences"]["infrastructure"])

        self.weights = Weights(DEFAULT_CANDIDATES[party]["weights"]["economy"],
                               DEFAULT_CANDIDATES[party]["weights"]["taxes"],
                               DEFAULT_CANDIDATES[party]["weights"]["healthcare"],
                               DEFAULT_CANDIDATES[party]["weights"]["education"],
                               DEFAULT_CANDIDATES[party]["weights"]["immigration"],
                               DEFAULT_CANDIDATES[party]["weights"]["environment"],
                               DEFAULT_CANDIDATES[party]["weights"]["crime"],
                               DEFAULT_CANDIDATES[party]["weights"]["government_size"],
                               DEFAULT_CANDIDATES[party]["weights"]["foreign_policy"],
                               DEFAULT_CANDIDATES[party]["weights"]["infrastructure"])

        self.traits = CandidateTraits(DEFAULT_CANDIDATES[party]["traits"]["charisma"],
                                      DEFAULT_CANDIDATES[party]["traits"]["debate_skill"],
                                      DEFAULT_CANDIDATES[party]["traits"]["media_skill"],
                                      DEFAULT_CANDIDATES[party]["traits"]["fundraising"],
                                      DEFAULT_CANDIDATES[party]["traits"]["organization"],
                                      DEFAULT_CANDIDATES[party]["traits"]["discipline"],
                                      DEFAULT_CANDIDATES[party]["traits"]["persuasion"],
                                      DEFAULT_CANDIDATES[party]["traits"]["leadership"],
                                      DEFAULT_CANDIDATES[party]["traits"]["authenticity"],
                                      DEFAULT_CANDIDATES[party]["traits"]["experience"],
                                      DEFAULT_CANDIDATES[party]["traits"]["risk_tolerance"],
                                      DEFAULT_CANDIDATES[party]["traits"]["coalition_building"])
                                    
        self.money = 0
        self.regional_popularity = {}

    def calculate_appeal_score(self):
        """Calculate overall candidate appeal based on traits (0-1 scale)."""
        trait_values = [
            self.traits.charisma,
            self.traits.debate_skill,
            self.traits.media_skill,
            self.traits.fundraising,
            self.traits.organization,
            self.traits.discipline,
            self.traits.persuasion,
            self.traits.leadership,
            self.traits.authenticity,
            self.traits.experience,
            self.traits.risk_tolerance,
            self.traits.coalition_building
        ]
        return np.mean(trait_values)

    def calculate_voter_affinity(self, voter):
        """Calculate how much a specific voter likes this candidate (0-1 scale)."""
        # Policy alignment component
        policy_match = (
            (1 - abs(voter.preferences.economy - self.preferences.economy) / 2) * voter.weights.economy +
            (1 - abs(voter.preferences.tax - self.preferences.tax) / 2) * voter.weights.tax +
            (1 - abs(voter.preferences.healthcare - self.preferences.healthcare) / 2) * voter.weights.healthcare +
            (1 - abs(voter.preferences.education - self.preferences.education) / 2) * voter.weights.education +
            (1 - abs(voter.preferences.immigration - self.preferences.immigration) / 2) * voter.weights.immigration +
            (1 - abs(voter.preferences.environment - self.preferences.environment) / 2) * voter.weights.environment +
            (1 - abs(voter.preferences.crime - self.preferences.crime) / 2) * voter.weights.crime +
            (1 - abs(voter.preferences.government_size - self.preferences.government_size) / 2) * voter.weights.government_size +
            (1 - abs(voter.preferences.foreign_policy - self.preferences.foreign_policy) / 2) * voter.weights.foreign_policy +
            (1 - abs(voter.preferences.infrastructure - self.preferences.infrastructure) / 2) * voter.weights.infrastructure
        ) / 10
        
        # Candidate traits appeal component
        candidate_appeal = self.calculate_appeal_score()
        
        # Combined affinity score (normalized to 0-1)
        voter_affinity = np.clip(0.7 * policy_match + 0.3 * candidate_appeal, 0, 1)
        return voter_affinity

    def calculate_regional_popularity(self, region):
        """Calculate candidate popularity in a specific region based on voter affinity."""
        if not region.voter_list:
            return 0.0
        
        total_affinity = sum(self.calculate_voter_affinity(voter) for voter in region.voter_list)
        regional_popularity = total_affinity / len(region.voter_list)
        
        # Store for reference
        self.regional_popularity[region.name] = regional_popularity
        return regional_popularity

    def get_regional_popularity(self, region_name):
        """Get stored regional popularity for a specific region."""
        return self.regional_popularity.get(region_name, 0.0)

class Party:
    def __init__(self, name):
        self.name = name
        self.popularity = DEFAULT_PARTY_PREFERENCES[name]["popularity"]
        self.preferences = Preferences(DEFAULT_PARTY_PREFERENCES[name]["preferences"]["economy"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["taxes"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["healthcare"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["education"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["immigration"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["environment"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["crime"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["government_size"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["foreign_policy"],
                                       DEFAULT_PARTY_PREFERENCES[name]["preferences"]["infrastructure"])
        
        self.weights = Weights(DEFAULT_PARTY_PREFERENCES[name]["weights"]["economy"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["taxes"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["healthcare"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["education"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["immigration"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["environment"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["crime"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["government_size"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["foreign_policy"],
                              DEFAULT_PARTY_PREFERENCES[name]["weights"]["infrastructure"])

        self.candidate = Candidate(name)

    def __repr__(self):
        return f"Party(name={self.name}, ideology={self.ideology})"